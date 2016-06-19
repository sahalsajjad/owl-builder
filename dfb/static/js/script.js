$(document).ready(function(){
        window.lookup = function(id){
            for( var key in classReference){
                try{
                    var premise = classReference[key]['id']== id;
                    if(premise){
                        
                        return key;
                    }
                }catch(err){
                    console.log(err.message);
                }    
            }
            return false;
        }
        window.findChildren = function(class_name, classReference){

            try{
                return classReference[class_name]["children"];
            }catch(err){
             
            }
        } 
        window.nestedTree = function( depth, parent_id, uniq){
            
            var un = uniq.toString();
            if(typeof(uniq) === 'object'){
                    un = uniq["id"];
            }
            $('#plus-'+un).hide();
            var sugar="";
            if(depth == 0){
                var sugar = "_";
            }
            $('#check_'+sugar+un).css('margin-left','25px');
            var treeview = document.getElementById(uniq);
            if(typeof(uniq) === 'object'){
                treeview = document.getElementById(uniq["id"]);
            }
            var parent_class = lookup(parent_id);
            
            var children = classReference[parent_class]["children"];
          
            for(var i=0; i< children.length; i++){
                var child_class = lookup(children[i]);
                var child_id = children[i].toString();
                var new_child_children = classReference[child_class]["children"];
                
                if(depth < 1){
                    var new_id = "_"+un+"_"+child_id;
                }else{
                    var new_id = un+"_"+child_id;
                }
                if(new_child_children.length > 0){
                    var upd_depth = depth + 1;
                        
                    treeview.innerHTML+="<br>";
                    
                    var space = (upd_depth*40).toString() +"px";
                        treeview.innerHTML+="<span id=\"space-"+new_id+"\"></span><span id=\"plus-"+new_id+"\""+"class=\"plus-button\""+"onclick=\"nestedTree("+upd_depth+","+child_id+","+new_id+")\">+"+
                        "</span>";
                       
                    $('#space-'+new_id).css('margin-left',space);    
                }

                else{
                    var upd_depth = depth + 1;
                    var space = (upd_depth*37.5).toString() +"px";
                    treeview.innerHTML+="<br><span id=\"em-"+new_id+"\" class=\"empty-space\"></span>";
                    $('#em-'+new_id).css('margin-left',space);    
                }
            treeview.innerHTML+="<input id=\"check_"+new_id+ "\" type=\"checkbox\">"+"<div class=\"data-holder\""+"id=\""+new_id+"\">"+child_class+"</div>";
            }
        }
        
        function printObjectKeys() {
            var treeview = document.getElementById('treeview');
            var key = data["0"];
            for(var i=0; i < key.length; i++){
                var cl = key[i]["class"];
                var children = key[i]["children"];
                
                var uniq =key[i]["id"].toString();

                if(children.length > 0){
                    treeview.innerHTML+=
                    "<span  id=\"plus-"+uniq+"\""+"class=\"plus-button\""+ 
                           "onclick=\"nestedTree("+0+","+key[i]["id"]+","+uniq+")\">+"+
                    "</span>";
                    
                }
                else{
                    treeview.innerHTML+="<span class=\"empty-space\"></span>";   
                }    
                var sugar="";

                treeview.innerHTML+=
                "<input id=\"check__"+uniq+  "\" type=\"checkbox\">"+
                "<div  class=\"data-holder\""+ 
                      "id=\""+uniq+"\">"+ cl.toString()+
                "</div>"+
                "<br>";
            }
        }
        printObjectKeys();
        window.SubmitForm = function(){
            var separator = "~~~~~";
            var send_data = {};
            var counter=0;
            $('#generated-form input').each(function() {
                var id = $(this).prop('id');
                var hierarchy = id.split("check");
                var id_list = hierarchy[1].split("_");
                var lookup_list = id_list.splice(2,id_list.length);
                var props = lookup_list[lookup_list.length-1].split("-");

                var classes = "";
                for (var i = 0; i< lookup_list.length-1 ; i++) {
                    if(i>0){
                        classes+=separator;
                    }
                    classes+=lookup(lookup_list[i]);
                    
                };
                var property = "NaP";
                var isProperty = "False";
                if(props.length > 1){
                    classes+=separator;
                    classes+=lookup(props[0]);
                    var property = props[props.length-1];
                    var isProperty="True";
                } 
                else{
                    classes+=separator;
                    classes+=lookup(lookup_list[lookup_list.length-1]);
                }   
               var val = $(this).prop('value');
               var temp=[];
               temp.push(classes);
               temp.push(val);
               temp.push(property);
               temp.push(isProperty);
               send_data[counter]=temp;
                counter+=1;
               
            });
            $('#generated-form select').each(function(){
                var id = $(this).prop('id');
                var hierarchy = id.split("check");
                var id_list = hierarchy[1].split("_");
                var lookup_list = id_list.splice(2,id_list.length);
                var props = lookup_list[lookup_list.length-1].split("-");

                var classes = "";
                for (var i = 0; i< lookup_list.length-1 ; i++) {
                    if(i>0){
                        classes+=separator;
                    }
                    classes+=lookup(lookup_list[i]);
                    
                };
                var property = "NaP";
                var isProperty = "False";
                if(props.length > 1){
                    classes+=separator;
                    classes+=lookup(props[0]);
                    var property = props[props.length-1];
                    var isProperty="True";
                } 
                else{
                    classes+=separator;
                    classes+=lookup(lookup_list[lookup_list.length-1]);
                }   
                var datatype = $(this).prop('value');
                for(var obj in send_data){
                    if(send_data[obj][2] === property){
                        
                        send_data[obj].push(datatype);
                    }
                } 
            });
            $.ajax({
                url: '/submit/form/',
                method: 'POST',
                data:{
                    "form_data":send_data
                },
                success:function(data){
                    window.location="/output/";
                }
        
            });
        }
        window.getProperties = function(form_class){
            
            return classReference[lookup(form_class)]["properties"];
        }
        window.prop_lookup = function(id){
            for( var key in propertyReference){
                try{
                    var premise = propertyReference[key] == id;
                    if(premise){
                        return key;
                    }
                }catch(err){
                    console.log(err.message);
                }    
            }
            return false;
        }
        window.generateForm = function(){
            var selected = [];
            $('#treeview input:checked').each(function() {
                selected.push($(this).attr('id'));
            });
            
            $('#empty-message').hide();
            var formarea = document.getElementById('form-area');
            var content="<div class=\"row\">";
            /* Form begins here */
            content+="<form action=\"#\" method=\"get\" id=\"generated-form\">";
            /* For each selected class */
            content+="<p class=\"notification\">&nbsp;&nbsp;&nbsp;&nbsp;For adding image/audio/video for a property, select any URI and enter the local address of the resource.</p>";
            for( var i=0; i < selected.length; i++ ){
                var elem = selected[i];

                content+="<div class=\"form-holder col-lg-11\" id=\"form-"+elem+"\">";
                /* form-group header begins */
                content+="<div class=\"form-title form-group\">";
                var hierarchy_list = elem.split("-");
                if(hierarchy_list.length > 1){
                   hierarchy_list = hierarchy_list[1].split("_")
                }
                else{
                    hierarchy_list = hierarchy_list[0].split("_");
                }
                var identifiers = hierarchy_list.splice(2, hierarchy_list.length );
                var form_class = identifiers[identifiers.length - 1];
                for(var j=0; j < identifiers.length - 1; j++){
                    var parent_class = identifiers[j];
                    content+="<span class=\"parent-crumb\">";
                    if(j>0){
                        content+=" / ";
                    }
                   content+=lookup(parent_class);
                    content+="</span>";
                }
                if(identifiers.length > 1){
                    content+=" / ";
                }
                var properties = getProperties(form_class)
                content+="<span class=\"class-crumb\">";
                content+=lookup(form_class);
                content+="</span>";
                /* Form-group header ends and the fields begin */

                content+="</div><div class=\"form-group\">";
                content+="Instance:<br><input type=\"text\" class=\"form-control\" id=\"value-"+elem+"\">";
                content+="</div>";
                if(properties.length > 0){
                    content+="<br><h4>Properties</h4>"
                }
                for(var j=0; j < properties.length; j++){
                  content+="<div class=\"form-group\">";
                  content+= prop_lookup(properties[j]);
                  content+=":<br>";
                  content+=" <select id=\""+elem+"-datatype-"+prop_lookup(properties[j])+"\" class=\"form-control form-control-2\">";
                  content+=     "<option value=\"xsd:string\">string</option>";
                  content+=     "<option value=\"xsd:boolean\">boolean</option>";
                  content+=     "<option value=\"xsd:decimal\">decimal</option>";
                  content+=     "<option value=\"xsd:integer\">integer</option>";
                  content+=     "<option value=\"xsd:dateTime\">date time</option>";
                  content+=     "<option value=\"xsd:time\">time</option>";
                  content+=     "<option value=\"xsd:date\">date</option>";
                  content+=     "<option value=\"xsd:anyURI\">any URI</option>";
                  content+="</select>"
                  content+="<input type=\"text\" class=\"form-control form-control-8\"";
                  content+=" id=\""+elem+"-prop-"+prop_lookup(properties[j])+"\">";
                  content+="</div>";                    
                }
                content+="</div>";
            }
            content+="<div class=\"col-lg-8\"><div class=\"col-lg-offset-5\"><button  onclick=\"SubmitForm()\" class=\"btn btn-info\">Submit Values</button></div>";
            content+="</form></div></div>";
            /* Form ends here */
            formarea.innerHTML=content;
        }
});