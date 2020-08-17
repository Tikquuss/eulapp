document.addEventListener('DOMContentLoaded', function(){ 
    /* Select */
    /*
    var defaut_model = "TF-IDF" //{{defaut_model|safe}}
    //document.getElementById(defaut_model).setAttribute('selected', "True")
    //*/

    /* Submit */
    document.getElementById("submit-boutton").addEventListener("click", function(){
        //eula1 = document.getElementById("eula-textarea").value
        //eula2 = document.getElementById("eula-textarea").value
        //console.log(eula1, eula2)
    });

    /*textarea*/
    document.getElementById("eula-textarea").addEventListener("focus", function(){
        //document.getElementById("id_docfile").style.disabled = "True"
        //console.log(document.getElementById("message").innerText, "===")
        //document.getElementById("message").innerText = "" 
    });

    /*docfile*/
    document.getElementById("id_docfile").addEventListener("focus", function(){
        //document.getElementById("eula-textarea").style.disabled = "True"
        //console.log(document.getElementById("message").innerText)
        //document.getElementById("message").innerText = ""
    });

}, false);


