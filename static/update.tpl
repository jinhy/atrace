<!DOCTYPE html>
<html>
	<head> 
        <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
		<title>update</title>
		<link href="/static/main.css" rel="stylesheet" type="text/css">
		<script src="/static/jquery.js" language="JavaScript" type="text/javascript"></script>
		<script src="/static/main.js" language="JavaScript" type="text/javascript"></script>
	</head>
	<body style="height:100%;" >
        <br/>
        <form action="/u" method="get">
            <input name="name" type="text" value='{{name}}' />
            <input  type="submit" value="查询" />
        </form>
        <br/>
        %if result:
            <table class="found" border="1" cellpadding="5" cellspacing="0"  width="80%">
                
                %if result['found']:
                    <tr style="font-weight: bold;background-color: gray;">
                        %for w in result['title'][1:]:
                        <td>{{w}}</td>
                        %end
                        <td>操作</td>
                        <td>操作</td>
                    </tr>
                    
                    %for line in result['found']:
                        <tr>
                            %for i in range(1,len(line)):
                            <td id="{{result['title'][i]}}">{{line[i]}}</td>
                            %end
                            <td id="delete" style="background-color: burlywood;cursor: pointer;" >删除</td>
                            <td id="edit" style="background-color: burlywood;cursor: pointer;">修改</td>
                        </tr>
                    %end
                %else:
                    <tr style="color:red">
                        <td>NOT FOUND!</td>
                    </tr>
                %end
            </table>
        %end
	</body>
</html>
