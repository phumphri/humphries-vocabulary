function login()
{
    var userNameElement = document.getElementById("un");
    
    parent.tocframe.h3.className = "show";      /*  Table of Contents   */
    
    parent.tocframe.ul.classname = "show"

    parent.tocframe.rd.className = "show";      /*  Random Definition   */
    parent.tocframe.rw.className = "show";      /*  Random  Word        */
    parent.tocframe.gw.className = "show"       /*  Word                */
    
    if (userNameElement.value == "Patrick") 
    {
        parent.tocframe.mw.className = "show";  /*  Maintain Word   */
    }
    else
    {
        parent.tocframe.mw.className = "hide";
    }
}