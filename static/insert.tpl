<!DOCTYPE html>
<html>
	<head> 
        <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
		<title>insert</title>
		<link href="/static/main.css" rel="stylesheet" type="text/css">
		<script src="/static/jquery.js" language="JavaScript" type="text/javascript"></script>
		<script src="/static/main.js" language="JavaScript" type="text/javascript"></script>
	</head>
	<body style="height:100%;" >
        <br/>
        <br/>
            <table class="found" border="1" cellpadding="5" cellspacing="0"  width="80%">
            
                <tr style="font-weight: bold;background-color: gray;">
                    %for w in result['title'][1:]:
                    <td>{{w}}</td>
                    %end
                    <td>操作</td>
                </tr>
                
                <tr>
                    
                    %for w in result['title'][1:]:
                    <td id={{w}}><textarea></textarea></td>
                    %end
                    <td id="insert" style="background-color: burlywood;cursor: pointer;">插入</td>
                </tr>
                <tr style="display:none">
                    
                    %for w in result['title'][1:]:
                    <td id={{w}}></td>
                    %end
                    <td >已插入</td>
                </tr>
            </table>
	</body>
</html>
