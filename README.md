# curbd
Manage configuration of apps via the consul service.

It populate's consul key/values like so.

Config files are stored like ENVIRONMENT/PROGRAM/CONFIG.json
where the curbd command is 
```
curbd $PROGRAM $CONFIG -e $ENVIRONMENT
```
and will populate keys in consul like
```
/PROGRAM/CONFIG/property
```

which then can be retrived by applications to obtain their configuration.
