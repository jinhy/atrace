<!DOCTYPE html>
<html>
	<head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
		<title>syscalls</title>
        <style>
        body {margin:0 auto;text-align: center;}
        table{margin:0 auto;text-align: center;}
        </style>
		<link href="/static/main.css" rel="stylesheet" type="text/css">
	</head>
	<body style="height:100%;" >
		<table class="found" border="1" cellpadding="5" cellspacing="0"  width="80%">
        
            <tr style="font-weight: bold;background-color: gray;">
                %for w in result['title'][1:]:
                <td>{{w}}</td>
                %end
            </tr>
            
            %for line in result['found']:
                <tr>
                    %for w in line[1:]:
                    <td>{{w}}</td>
                    %end
                </tr>
            %end
            %for w in result['unfound']:
                <tr style="color:red">
                    <td>{{w}}</td>
                    <td>NOT FOUND!</td>
                </tr>
            %end
        </table>
	</body>
</html>
