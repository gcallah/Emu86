/**
 * Created by Varun on 19/06/17.
 */

function AlertError()
{
    var raised=document.getElementById("error")

    if(raised)
    {
        raised=raised.value;
        if (raised != "") 
        {
            alert(document.getElementById("error").value);
        }
    }
}

function selectSample()
{
    selectBar = document.getElementsByName("sample")[0];
    var selected = selectBar.options[selectBar.selectedIndex].value
    var flav = document.getElementsByName("flavor")[0];
    if (flav){
        if (selected == "none"){
            document.getElementById("id_code").value = "";
        }
        else if (selected == "addTwo") {
            addTwo(flav.value);
        }
        else if (selected == "arithExpr") {
            arithExpr(flav.value);
        }
        else if (selected == "log") {
            log(flav.value);
        }
        else if (selected == "modify") {
            modify(flav.value);
        }
        else if (selected == "loop") {
            loop(flav.value);
        }
        else if (selected == "avg") {
            avg(flav.value);
        }
        else if (selected == "celFah") {
            celFah(flav.value);
        }
        else if (selected == "sqrt") {
            sqrt(flav.value);
        }
        else if (selected == "area") {
            area(flav.value);
        }
        else if (selected == "power") {
            power(flav.value);
        }
        else if (selected == "arithShift") {
            arithShift(flav.value);
        }
        else if (selected == "data") {
            data(flav.value);
        }
        else if (selected == "keyInterrupt") {
            keyInterrupt(flav.value);
        }
        else if (selected == "array") {
            array(flav.value);
        }
    }
}

function checkForScript()
{
    data = document.getElementById("id_code").value;
    if (data.indexOf("<script>") != -1){
        var temp_val = data.split("<script>");
        data = temp_val.join("");
    }
    if (data.indexOf("</script>") != -1){
        var temp_val = data.split("</script>");
        data = temp_val.join("");
    }
    document.getElementById("id_code").value = data;
}

function loadcode()
{
    if(sessionStorage.loadonce)
    {
        AlertError();
        var instr = document.getElementsByName("last_instr")[0];
        var mips_ip = document.getElementsByName("PC");
        var intel_ip = document.getElementsByName("EIP");
        var ip_val = null;
        var hex_or_dec = null
        var radios = document.getElementsByName("base");
        for (var index = 0; index < radios.length; index++) {
            if (radios[index].checked) {
                hex_or_dec = radios[index].value;
                break;
            }
        }
        if (mips_ip.length != 0){
            if (hex_or_dec == "hex") {
                ip_val = parseInt(mips_ip[0].value, 16)/4;
            }
            else {
                ip_val = parseInt(mips_ip[0].value)/4;
            }
        }
        else if (intel_ip.length != 0) {
            if (hex_or_dec == "hex") {
                ip_val = parseInt(intel_ip[0].value, 16);
            }
            else {
                ip_val = parseInt(intel_ip[0].value);
            }
        }
        if (instr && ip_val) {
            var input = document.getElementById("id_code");
            var countCode = 0;
            var countRepeats = 0;
            var codeArray = input.value.split("\n");
            var textArea = true; 
            if (instr.value != "") {
                for (var index = 0; index < codeArray.length; index++) {
                    var string = codeArray[index].trim();
                    if (countCode == ip_val){
                        break;
                    }
                    if (string == ".data"){
                        textArea = false;
                        continue;
                    }
                    else if (string == ".text"){
                        textArea = true;
                        continue;
                    }
                    if (!(string === "") && textArea && string[0] != ";"){
                        countCode++; 
                    }
                    if (string == instr.value){
                        countRepeats++;
                    }
                }
                input.focus();
                var startIndex = 0;
                for (var time = 0; time < countRepeats; time++) {
                    startIndex = input.value.indexOf(instr.value, startIndex) 
                                 + instr.value.length;
                }
                startIndex -= instr.value.length;
                input.setSelectionRange(startIndex, 
                       startIndex + instr.value.length);
            }
        }
        return;
    }
    else
    {
        sessionStorage.loadonce=1;
        code = localStorage.Code;
        if(code!=undefined || code!=null) {
            document.getElementById("id_code").value = code;
        }
    }
}

function Savecode()
{
    var file_name = prompt("Please enter file name to save as, ending in .asm or .bin: ");
    if (file_name == ""){
        alert("Invalid file name");
    }
    else if (file_name.length < 5){
        alert("Invalid file name: " + file_name);
    }
    else if (file_name.slice(file_name.length - 4) != ".asm" && file_name.slice(file_name.length - 4) != ".bin") {
        alert("Invalid file name: " + file_name);
    }
    else {
        data = document.getElementById("id_code").value;
        var file_blob = new Blob([data], {type: 'text/plain'});
        if (window.navigator.msSaveOrOpenBlob) {
            window.navigator.msSaveOrOpenBlob(file_blob, file);
        }
        else {
            var anchor = document.createElement('a'),
            url = URL.createObjectURL(file_blob);
            anchor.href = url;
            anchor.download = file_name;
            document.body.appendChild(anchor);
            anchor.click();
            document.body.removeChild(anchor);
            window.URL.revokeObjectURL(url);  
        }
    }
}


function convert(name,value)
{
    var message= "Binary value of " + " " + name + ": ";
    var value1=parseInt(value)
    if(value1>=0) {

        message=message+((value1).toString(2));
        alert(message);
    }
    else
    {
        message=message+((value1>>>0).toString(2));
        alert(message);
    }
}