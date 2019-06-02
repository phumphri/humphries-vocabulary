function bindings() 
{
    var hs = document.getElementById('hs')      /*  Hide Spelling   */
    var hd = document.getElementById('hd')      /*  Hide Definition */

    var ws = document.getElementById("ws")      /*  Word Spelling   */
    var wd = document.getElementById("wd")      /*  Word Definition */
    var wg = document.getElementById("wg")      /*  Word Grammar    */
    var we = document.getElementById("we")      /*  Word Example    */

    var ms = document.getElementById("ms")      /*  My Spelling     */
    var md = document.getElementById("md")      /*  My Definition   */

    var wa = document.getElementById("wa")      /*  Word Attempts   */
    var wc = document.getElementById("wc")      /*  Word Correct    */
    var ww = document.getElementById("ww")      /*  Word Wrong      */
    var wp = document.getElementById("wp")      /*  Word Percentage */
    
    var hostAndPort = location.host;            /*  Host server and port.   */

    var st = document.getElementById("st")      /*  Status Field    */

    var aw = document.getElementById("aw")      /*  Add Word Button     */
    var uw = document.getElementById("uw")      /*  Update Word Button  */
    var dw = document.getElementById("dw")      /*  Delete Word Button  */
    var cw = document.getElementById("cw")      /*  Clear Word Button   */

    if (hostAndPort == '127.0.0.1:5000')        /*  Hide maintenance in the wild.   */
    {
        aw.className = "visible"
        uw.className = "visible"
        dw.className = "visible"
        cw.className = "visible"
    }
    else
    {
        aw.className = "hidden"
        uw.className = "hidden"
        dw.className = "hidden"
        cw.className = "hidden"
    }
}