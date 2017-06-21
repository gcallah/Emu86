/**
 * Created by Varun on 19/06/17.
 */



             function loadcode()
                {
                    if(sessionStorage.loadonce)
                    {
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
                    if(confirm("Do you want to save this code?")) {
                        data = document.getElementById("id_code").value;
                        try {
                            localStorage.Code=data;
                            alert("Your code was saved successfully.");
                        }
                        catch(exception)
                        {
                            alert("An unknown error occured, please try again.");

                        }
                    }
                }

                var raised=document.getElementById("error")

                if(raised)
                {
                    raised=raised.value;
                    alert(raised);
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

