# RUCTFE 2019 Radio Exploit / Writeup

This was the exploit I used to capture flags from the Radio service.
I noticed early on that the JWT Secret was generated in a predictable way. The following script was
used to generate the secret key used to sign the JWT.

```bash
#!/bin/bash
set -e

generate_key() {
    declare -r key_path=$1
    echo "$(date +\"%s\")$key_path"
    echo -n "$(date +\"%s\")$key_path" | sha256sum | awk '{print $1}' > $key_path
}

declare -r jwt_secret_path="${SECRET_PATH%/}/jwt_secret"
declare -r session_key="${SECRET_PATH%/}/session_key"

generate_key $jwt_secret_path
generate_key $session_key
```

Problem here is the `"$(date +\"%s\")$key_path"` that is fed to sha256sum. It's easy to bruteforce too, only requiring a few thousand offline attempts.

To patch I initially changed the secret by just adding a salt.

To exploit:

1. Register new user, log in and create a api token. Later I pipelined this to all hosts with the `register.py` script.
2. Take the API token, and bruteforce it with the `radio-auth.so` plugin. I wrote the `crack` golang program for this. First for a single token, then for a file of them. I was surprised how quick it was to bruteforce all ~103 hosts.
3. With the now known secret+host, my attack was to visit the `/frontend-api/our-users/` route, get the last 20 users, then get the playlist for each.
   If I was lucky, there would be a flag in the playlist. The `exfil.py` script took care of this.

Probably it would have been smart to reverse `radio-auth.so` and figure out what it actually does. I'm not confident in my reversing skills though, so I thought this would take too long.

Because we were still getting pwned, to mitigate it fully I replaced the entire JWT signing/parsing mechanism. This took a bit too long though, and most likely they were using another vulnerability.

The only optimization I did here was to pipeline the process. In the end I just ran 4 `exfil.py` worker scripts on different target lists.

## Another vuln

Our service still continued to get exploited though, I'm pretty sure the following "share hash" on the playlist was abused. Also what I saw a lot of
spam too in the logs. In the very last minute I uploaded a fix which added a salt though. It's the thought that matters.

```go
func (p *Playlist) HS() string {
	return fmt.Sprintf("%x", sha256.Sum256([]byte(fmt.Sprintf("playlist:{%d}:{%t}:{%d}:{&b}", p.ID, p.Private, p.UserID))))
}
```
