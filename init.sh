#!/usr/bin/env sh
# Fix /dev/stdout permissions error

if [ "$(id -u)" -eq 0 ]; then
  groupadd application               \
        --gid 1000
  useradd application                \
        --base-dir /app              \
        --home-dir /home/application \
        --create-home                \
        --uid 1000                   \
        --gid 1000                   \
        --system
  gpasswd -a application tty
  export USER='application'
else
  export USER="$(whoami)"
fi

echo "$(env)"

chmod o+w /dev/stdout /dev/stderr

# Fix supervisor pid permissions error
for pid in \
  /var/run/supervisord.pid
do
  touch "$pid"
  chown "$USER:$USER" "$pid"
done

chown "$USER:$USER" -R /app

/usr/local/bin/supervisord -c /etc/supervisord.conf
