<html>
<head>
</head>
<body>
<div>
<ul>
    % for service, hosts in services.items():
    <li>
        {{service}}
        % for host in hosts:
        <ul>  
            <li>
             {{host}}
            </li>
        </ul>
        % end
    </li>
    % end
</ul>
</div>
</body>
</html>