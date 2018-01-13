<?php
/* Override Servers array */
$cfg['Servers'] = [
    1 => [
        'auth_type' => 'config',
        'socket'=> '/var/run/sock/mysql5.sock',
        'verbose' => 'MySQL 5 Server',
        'user'=> 'root',
        'password'=> 'root',
    ],
];
