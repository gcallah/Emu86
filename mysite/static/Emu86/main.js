/**
 * Created by Varun on 19/06/17.
 * Edited by Cindy
 */


function AlertError()
{
    let raised=document.getElementById("error");

    if(raised)
    {
        raised=raised.value;
        if (raised !== "")
        {
            alert(document.getElementById("error").value);
        }
    }
}

function selectSample()
{
    selectBar = document.getElementsByName("sample")[0];
    const selected = selectBar.options[selectBar.selectedIndex].value;
    const flav = document.getElementsByName("flavor")[0];
    const base = document.getElementsByName("base")[0].value;
    if (flav && base === "dec"){
        if (selected === "none"){
            document.getElementById("id_code").value = "";
        }
        else if (selected === "addTwo") {
            addTwo(flav.value);
        }
        else if (selected === "arithExpr") {
            arithExpr(flav.value);
        }
        else if (selected === "float_addition") {
            float_addition(flav.value);
        }
        else if (selected === "log") {
            log(flav.value);
        }
        else if (selected === "modify") {
            modify(flav.value);
        }
        else if (selected === "loop") {
            loop(flav.value);
        }
        else if (selected === "avg") {
            avg(flav.value);
        }
        else if (selected === "celFah") {
            celFah(flav.value);
        }
        else if (selected === "sqrt") {
            sqrt(flav.value);
        }
        else if (selected === "area") {
            area(flav.value);
        }
        else if (selected === "power") {
            power(flav.value);
        }
        else if (selected === "arithShift") {
            arithShift(flav.value);
        }
        else if (selected === "data") {
            data(flav.value);
        }
        else if (selected === "keyInterrupt") {
            keyInterrupt(flav.value);
        }
        else if (selected === "array") {
            array(flav.value);
        }
        else if (selected === "dataAccess") {
            dataAccess(flav.value);
        }
        else if (selected === "data_fp") {
            data_fp(flav.value);
        }
        else if (selected === "power_fp") {
            power_fp(flav.value);
        }

        else if (selected === "area_fp") {
            area_fp(flav.value);
        }
        else if (selected === "addTwo_fp") {
            addTwo_fp(flav.value);
        }
        else if (selected === "celFah_fp") {
            celFah_fp(flav.value);
        }
    }
    else if (flav && base === "hex"){
        if (selected === "none"){
            document.getElementById("id_code").value = "";
        }
        else if (selected === "addTwo") {
            addTwo_hex(flav.value);
        }
        else if (selected === "arithExpr") {
            arithExpr_hex(flav.value);
        }
        else if (selected === "log") {
            log_hex(flav.value);
        }
        else if (selected === "modify") {
            modify_hex(flav.value);
        }
        else if (selected === "loop") {
            loop_hex(flav.value);
        }
        else if (selected === "avg") {
            avg_hex(flav.value);
        }
        else if (selected === "celFah") {
            celFah_hex(flav.value);
        }
        else if (selected === "sqrt") {
            sqrt_hex(flav.value);
        }
        else if (selected === "area") {
            area_hex(flav.value);
        }
        else if (selected === "power") {
            power_hex(flav.value);
        }
        else if (selected === "arithShift") {
            arithShift_hex(flav.value);
        }
        else if (selected === "data") {
            data_hex(flav.value);
        }
        else if (selected === "keyInterrupt") {
            keyInterrupt_hex(flav.value);
        }
        else if (selected === "array") {
            array_hex(flav.value);
        }
        else if (selected === "dataAccess") {
            dataAccess_hex(flav.value);
        }
        else if (selected === "data_fp") {
            data_fp(flav.value);
        }
        else if (selected === "power_fp") {
            power_fp(flav.value);
        }

        else if (selected === "area_fp") {
            area_fp(flav.value);
        }
        else if (selected === "addTwo_fp") {
            addTwo_fp(flav.value);
        }
        else if (selected === "celFah_fp") {
            celFah_fp(flav.value);
        }
    }
}

function checkForScript()
{
    let data = document.getElementById("id_code").value;
    if (data.indexOf("<script>") !== -1){
        data = data.replace("<script>", "");
    }
    if (data.indexOf("</script>") !== -1){
        data = data.replace("</script>", "");
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
        const code = localStorage.Code;
        if(code !== undefined || code !== null) {
            document.getElementById("id_code").value = code;
        }
    }
}

function highlightCode(){
    const instr = document.getElementsByName("last_instr")[0];
    let lastInstr = instr.value;
    let line_num;
    if (lastInstr.indexOf("Line") !== -1){
        line_num = parseInt(lastInstr.substring(5, lastInstr.indexOf(":")))
        lastInstr = lastInstr.substring(lastInstr.indexOf(":") + 1)
    }
    if (lastInstr.indexOf(": Exiting program") !== -1){
        lastInstr = lastInstr.substring(0, lastInstr.indexOf(": Exiting program"));
    }
    if (instr && lastInstr) {
        const input = document.getElementById("id_code");
        const codeArray = input.value.split("\n");
        let startIndex = 0;
        let lineLength = 0;
        for (let index = 0; index < codeArray.length; index++) {
            lineLength = codeArray[index].length;
            if (index === line_num - 1){
                break;
            }
            startIndex += codeArray[index].length + 1;
            // the extra + 1 is to take the new line character into account
        }
        input.focus();
        startIndex += lineLength - lastInstr.length + 1;
        input.setSelectionRange(startIndex, startIndex + lastInstr.length);
    }
}

function validName(flavor, fileName){
    const fileExt = {
        "mips_asm": [".asm", ".txt"],
        "mips_mml": [".txt"],
        "mips": [".asm"]
    }

    if (fileName.length < 5){
        return false
    }
    else if(flavor in Object.keys(fileExt) && !(fileName.slice(fileName.length - 4) in fileExt[flavor])){
        return false
    }
    return true
}

function Savecode()
{
    const flav = document.getElementsByName("flavor")[0].value;
    let fileName = null;
    if (flav === "mips_asm"){
        fileName = prompt("Please enter file name to save as, ending in .asm or .txt (for machine code): ");
    }
    else if (flav === "mips_mml"){
        fileName = prompt("Please enter file name to save as, ending in .txt (for machine code): ");
    }
    else{
        fileName = prompt("Please enter file name to save as, ending in .asm: ");
    }
    if (fileName === null){
        alert("Save cancelled");
    }
    else if (fileName === ""){
        alert("Invalid file name");
    }
    else if (!validName(flav, fileName)){
        alert("Invalid file name: " + fileName);
    }
    else {
        let data = null;
        if (fileName.slice(fileName.length - 4) === ".asm"){
            data = document.getElementById("id_code").value;
        }
        else{
            data = document.getElementsByName("bit_code")[0].value;
        }
        const fileBlob = new Blob([data], {type: 'text/plain'});
        if (window.navigator.msSaveOrOpenBlob) {
            window.navigator.msSaveOrOpenBlob(fileBlob, file);
        }
        else {
            const anchor = document.createElement('a'),
            url = URL.createObjectURL(fileBlob);
            anchor.href = url;
            anchor.download = fileName;
            document.body.appendChild(anchor);
            anchor.click();
            document.body.removeChild(anchor);
            window.URL.revokeObjectURL(url);
        }
    }
}

function resolveAfter1HalfSeconds() {
    return new Promise(resolve => {
      setTimeout(() => {
        resolve('resolved');
      }, 3000);
    });
}

async function slowCall() {
    await resolveAfter1HalfSeconds();
}

async function SubmitForm(demo_on = false, pause = false){
    if ((demo_on) && (pause === false)) {
        await slowCall();
    } else if (demo_on === true && pause === true) {
        debugger;
    }

    document.getElementById("codeForm").submit();
    document.getElementById("clear-button").disabled="true";
    document.getElementById("run-button").disabled="true";
    document.getElementById("save-button").disabled="true";
    document.getElementById("step-button").disabled="true";
    document.getElementById("demo-button").disabled="true";
    document.getElementById("pause-button").disabled="true";
}

function clearButton(){
    if (document.readyState === "complete") {
        if (document.getElementById("clear-button").hasAttribute("disabled") === false){
            document.getElementsByName("button_type")[0].value = "clear";
            SubmitForm();
        }
    }
}

function runButton(){
    if (document.readyState === "complete") {
        if (document.getElementById("run-button").hasAttribute("disabled") === false){
            document.getElementsByName("button_type")[0].value = "run";
            SubmitForm();
        }
    }
}

function stepButton(){
    if (document.readyState === "complete") {
        if (document.getElementById("step-button").hasAttribute("disabled") === false){
            document.getElementsByName("button_type")[0].value = "step";
            SubmitForm();
        }
    }
}

function demoButton(){
    if (document.readyState === "complete") {
        if (document.getElementById("demo-button").hasAttribute("disabled") === false){
            document.getElementsByName("button_type")[0].value = "demo";
            SubmitForm();
        }
    }
}

function pauseButton(){
    if (document.readyState === "complete") {
        if (document.getElementById("pause-button").hasAttribute("disabled") === false){
            document.getElementsByName("button_type")[0].value = "pause";
            SubmitForm();
        }
    }
}

function convert(name,value)
{
    let message= `Binary value of ${name}: `;
    const hexOrDec = document.getElementsByName("base")[0].value;
    let value1 = null;

    if (hexOrDec === "hex"){
        value1=(parseInt(value, 16));
    }
    else{
        value1=parseInt(value.toString(), 10);
    }
    if(value1>=0) {
        message=message+((value1).toString(2));
        alert(message);
    }
    else
    {
        message=message+((value1 >>> 0).toString(2));
        alert(message);
    }
}

function parseIntegerBase(val, base){
    for (let i = 0; i < val.length; i++){
        if (isNaN(parseInt(val.charAt(i), base))) {
            return false;
        }
    }
    return true;
}

function AddMem()
{
    let memData = document.getElementsByName("mem_data")[0].value;
    let loc = document.getElementById("memText").value;
    const val = document.getElementById("valueText").value;
    let repeat = document.getElementById("repeatText").value;
    const flav = document.getElementsByName("flavor")[0].value;
    const base = document.getElementsByName("base")[0].value;
    if (loc === ""){
        alert("Cannot set an invisible location");
        document.getElementById("memText").value = "";
        document.getElementById("valueText").value = "";
        document.getElementById("repeatText").value = "1";
        return;
    }
    else if (val === ""){
        alert("Cannot set using an invisible value");
    }

    if (base === "dec") {
        if (!parseIntegerBase(val, 10)) {
            alert("Not a valid value for decimal number system");
            document.getElementById("memText").value = "";
            document.getElementById("valueText").value = "";
            document.getElementById("repeatText").value = "1";
            return;
        }
    }

    else if (!parseIntegerBase(val, 16)) {
            alert("Not a valid value for hexadecimal number system");
            document.getElementById("memText").value = "";
            document.getElementById("valueText").value = "";
            document.getElementById("repeatText").value = "1";
            return;
        }

    if (repeat !== ""){
        repeat = parseInt(repeat);
    }
    else {
        repeat = 0;
    }
    let currentHtml = document.getElementById("memory-table").innerHTML;
    let addHtml = "";
    for (let i = 0; i < repeat; i++) {
        if (inStack(loc)){
            setStackLoc(loc, val);
        }
        else{
            if (currentHtml.indexOf('name="' + loc + '"') !== -1) {
                const findValue = currentHtml.indexOf('value="', currentHtml.indexOf('name="' + loc + '"'));
                const findEnd = currentHtml.indexOf('"', findValue);
                currentHtml = currentHtml.substring(0, findValue + 7) + val.toString() + currentHtml.substring(findEnd);
                const locationIndex = memData.indexOf(loc + ":");
                const commaIndex = memData.indexOf(",", locationIndex);
                memData = memData.substring(0, locationIndex + loc.length + 1) + val + memData.substring(commaIndex);
            }
            else {
                addHtml += "<tr><td id='mem-loc' style='height:5px'>" + loc + "</td>";
                addHtml += "<td id='contents' style='height:5px'>";
                addHtml += "<input id='mem-cont' name='" + loc + "' value='" + val.toString() + "' size ='5' readonly='readonly' style='background-color:#eff;'></td></tr>";
                memData += loc + ":" + val + ", ";
            }
        }
        let location = null;
        if (flav !== "mips_asm" && flav !== "mips_mml") {
            location = parseInt(loc, 16) + 1;
        }
        else {
            location = parseInt(loc, 16) + 4;
        }
        loc = location.toString(16).toUpperCase();
    }
    document.getElementById("memory-table").innerHTML = currentHtml + addHtml;
    document.getElementsByName("mem_data")[0].value = memData;

    // reset the values
    document.getElementById("memText").value = "";
    document.getElementById("valueText").value = "";
    document.getElementById("repeatText").value = "1";
}

function setStackLoc(loc, value){
    const stackCell = document.getElementsByName(loc)[0];
    stackCell.value = value;
}

function inStack(location){
    const numLoc = parseInt(location, 16);
    if (numLoc >= Math.pow(2, 8) && numLoc < Math.pow(2, 9)){
        return true;
    }
    return false;
}

function displayHelp(buttonType){
    const messages = {
        clear: "Reset register and memory values.",
        step: "Execute one instruction at a time.",
        run: "Execute all lines of code.",
        demo: "Demo code line by line.",
        save: "Save code as a file.",
        pause: "Pauses and resets code where demo leaves off from."
    }

    const spanNode = document.getElementById("help-desc");
    spanNode.classList.toggle("show");
    spanNode.textContent = messages[buttonType];
}

function hideHelp(){
    document.getElementById("help-desc").classList.toggle("show");
}
