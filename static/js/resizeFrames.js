function resizeFrames()
{
    try 
    {
        var w = screen.availWidth;
        var h = screen.availHeight;
        
        var lf = document.getElementById("lf");     /*  Logo Frame      */
        var bf = document.getElementById("bf");     /*  Banner Frame    */
        var tf = document.getElementById("tf");     /*  TOC Frame       */
        var vf = document.getElementById("vf");     /*  View Frame      */
        
        var leftFrameWidths = (w * 0.15) + "px";
        var rightFrameWidths = (h * 0.85) + "px";
        var bottomFrameHeights = (h - 125) + "px";
        
        lf.width = leftFrameWidths;
        bf.width = rightFrameWidths;
        tf.width = leftFrameWidths;
        vf.width = rightFrameWidths;
        tf.height = bottomFrameHeights;
        vf.height = bottomFrameHeights;
    }
    catch (e)
    {
        alert("resizeFrames() threw an Error:  " + e.toString());
    }
}