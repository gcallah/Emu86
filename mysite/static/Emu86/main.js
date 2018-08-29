/**
 * Created by Varun on 19/06/17.
 * Edited by Cindy
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
        else if (selected == "dataAccess") {
            dataAccess(flav.value);
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

function highlightCode(){
    var instr = document.getElementsByName("last_instr")[0];
    var lastInstr = instr.value;
    if (lastInstr.indexOf(": Exiting program") != -1){
        lastInstr = lastInstr.substring(0, lastInstr.indexOf(": Exiting program"));
    }
    var mips_ip = document.getElementsByName("PC");
    var intel_ip = document.getElementsByName("EIP");
    var ip_val = null;
    var hex_or_dec = null;
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
                if (string == lastInstr){
                    countRepeats++;
                }
            }
            input.focus();
            var startIndex = 0;
            for (var time = 0; time < countRepeats; time++) {
                startIndex = input.value.indexOf(lastInstr, startIndex) 
                             + lastInstr.length;
            }
            startIndex -= lastInstr.length;
            input.setSelectionRange(startIndex, 
                   startIndex + lastInstr.length);
        }
    }
}

function Savecode()
{
    var flav = document.getElementsByName("flavor")[0].value;
    var file_name = null;
    if (flav == "mips_asm"){
        file_name = prompt("Please enter file name to save as, ending in .asm or .txt (for machine code): ");
    }
    else if (flav == "mips_mml"){
        file_name = prompt("Please enter file name to save as, ending in .txt (for machine code): ");
    }
    else{
        file_name = prompt("Please enter file name to save as, ending in .asm: ");
    }
    if (file_name == null){
        alert("Save cancelled");
    }
    else if (file_name == ""){
        alert("Invalid file name");
    }
    else if (file_name.length < 5){
        alert("Invalid file name: " + file_name);
    }
    else if (flav == "mips_asm" && file_name.slice(file_name.length - 4) != ".asm" && file_name.slice(file_name.length - 4) != ".txt" ) {
        alert("Invalid file name: " + file_name);
    }
    else if (flav == "mips_mml" && file_name.slice(file_name.length - 4) != ".txt" ) {
        alert("Invalid file name: " + file_name);
    }
    else if (flav != "mips" && file_name.slice(file_name.length - 4) != ".asm"){
        alert("Invalid file name: " + file_name);
    }
    else {
        data = null;
        if (file_name.slice(file_name.length - 4) == ".asm"){
            data = document.getElementById("id_code").value;
        }
        else{
            data = document.getElementsByName("bit_code")[0].value;
        }
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

async function SubmitForm(demo_on = false){
    if (demo_on){
        await slowCall()
    }
    document.getElementById("codeForm").submit();
    document.getElementById("clear-button").disabled="true";
    document.getElementById("run-button").disabled="true";
    document.getElementById("save-button").disabled="true";
    document.getElementById("step-button").disabled="true";
    document.getElementById("demo-button").disabled="true";
}

function clearButton(){
    if (document.readyState == "complete") {
        if (document.getElementById("clear-button").hasAttribute("disabled") == false){
            document.getElementsByName("button_type")[0].value = "clear";
            SubmitForm();
        }
    }
}

function runButton(){
    if (document.readyState == "complete") {
        if (document.getElementById("run-button").hasAttribute("disabled") == false){
            document.getElementsByName("button_type")[0].value = "run";
            SubmitForm();
        }
    }
}

function stepButton(){
    if (document.readyState == "complete") {
        if (document.getElementById("step-button").hasAttribute("disabled") == false){
            document.getElementsByName("button_type")[0].value = "step";
            SubmitForm();
        }
    }
}

function demoButton(){
    if (document.readyState == "complete") {
        if (document.getElementById("demo-button").hasAttribute("disabled") == false){
            document.getElementsByName("button_type")[0].value = "demo";
            SubmitForm();
        }
    }
}

function convert(name,value)
{
    var message= "Binary value of " + " " + name + ": ";
    var hex_or_dec = null;
    var radios = document.getElementsByName("base");
    for (var index = 0; index < radios.length; index++) {
        if (radios[index].checked) {
            hex_or_dec = radios[index].value;
            break;
        }
    }
    var value1 = null;
    if (hex_or_dec == "hex"){
        value1=parseInt(value, 16);
    }
    else{
        value1=parseInt(value);
    }
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

function parseIntegerBase(val, base){
    for (var i = 0; i < val.length; i++){
        if (isNaN(parseInt(val.charAt(i), base))) {
            return false;
        }
    }
    return true;
}

function AddMem()
{
    mem_data = document.getElementsByName("mem_data")[0].value;
    var loc = document.getElementById("memText").value;
    var val = document.getElementById("valueText").value;
    var repeat = document.getElementById("repeatText").value;
    var flav = document.getElementsByName("flavor")[0].value;
    var base = document.getElementsByName("base")[0].value;
    if (loc == ""){
        alert("Cannot set an invisible location");
        document.getElementById("memText").value = "";
        document.getElementById("valueText").value = "";
        document.getElementById("repeatText").value = "1";
        return;
    }
    else if (val == ""){
        alert("Cannot set using an invisible value");
    }

    if (base == "dec") {
        if (!parseIntegerBase(val, 10)) {
            alert("Not a valid value for decimal number system");
            document.getElementById("memText").value = "";
            document.getElementById("valueText").value = "";
            document.getElementById("repeatText").value = "1";
            return;
        }
    }

    else {
        if (!parseIntegerBase(val, 16)) {
            alert("Not a valid value for hexadecimal number system");
            document.getElementById("memText").value = "";
            document.getElementById("valueText").value = "";
            document.getElementById("repeatText").value = "1";
            return;
        }
    }

    if (repeat != ""){
        repeat = parseInt(repeat);
    }
    else {
        repeat = 0;
    }
    var current_html = document.getElementById("memory-table").innerHTML;
    var add_html = "";
    for (var i = 0; i < repeat; i++) {
        if (current_html.indexOf('name="' + loc + '"') != -1) {
            var find_value = current_html.indexOf('value="', current_html.indexOf('name="' + loc + '"'));
            var find_end = current_html.indexOf('"', find_value);
            current_html = current_html.substring(0, find_value + 7) + val.toString() + current_html.substring(find_end);
            var location_index = mem_data.indexOf(loc + ":");
            var comma_index = mem_data.indexOf(",", location_index);
            mem_data = mem_data.substring(0, location_index + loc.length + 1) + val + mem_data.substring(comma_index);
        }
        else {
            add_html += "<tr><td id='mem-loc' style='height:5px'>" + loc + "</td>";
            add_html += "<td id='contents' style='height:5px'>"
            add_html += "<input id='mem-cont' name='" + loc + "' value='" + val.toString() + "' size ='5' readonly='readonly' style='background-color:#eff;'></td></tr>";
            mem_data += loc + ":" + val + ", ";
        }
        var location = null;
        if (flav != "mips_asm" && flav != "mips_mml") {
            location = parseInt(loc, 16) + 1;
        }
        else {
            location = parseInt(loc, 16) + 4;
        }
        loc = location.toString(16).toUpperCase();
    }
    document.getElementById("memory-table").innerHTML = current_html + add_html;
    document.getElementsByName("mem_data")[0].value = mem_data;

    // reset the values
    document.getElementById("memText").value = "";
    document.getElementById("valueText").value = "";
    document.getElementById("repeatText").value = "1";
}

function resolveAfter1HalfSeconds() {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve('resolved');
    }, 1500);
  });
}

async function slowCall() {
  var result = await resolveAfter1HalfSeconds();
}

function displayHelp(button_type){
    var string = "";
    if (button_type == "clear"){
        string = "Reset register and memory values.";
    }
    else if (button_type == "step"){
        string = "Execute one instruction at a time.";
    }
    else if (button_type == "run"){
        string = "Execute all lines of code.";
    }
    else if (button_type == "demo"){
        string = "Demo code line by line.";
    }
    else if (button_type == "save"){
        string = "Save code as a file.";
    }

    var spanNode = document.getElementById("help-desc");
    spanNode.classList.toggle("show");
    spanNode.textContent = string;
}

function hideHelp(){
    document.getElementById("help-desc").classList.toggle("show");
}
