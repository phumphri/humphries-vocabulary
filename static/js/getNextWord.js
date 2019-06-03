function getNextWord()
{
    hideFields()

    st.value = "Getting next word.  Please wait."; 

    // If the browser does not support the XMLHttpRequest object, do nothing.
    if (!window.XMLHttpRequest)
    {
        st.value = "window.XMLHttpRequest failed.  Call Patrick.";
        return;
    }
    
    // Encode the user input as query parameters in a URL.
    var hostAndPort = location.host
    if (hostAndPort == '127.0.0.1:5000')
    {
        url = "http://" + hostAndPort + "/next_word/" + ws.value
    }
    else
    {
        url = "https://" + hostAndPort + "/next_word/" + ws.value
    }
    
    // Fetch the contents of that URL using the XMLHttpRequest object.
    var request = new XMLHttpRequest();
    
    if (!request)
    {
        st.value = "new XMLHttpRequest() returned null.  Call Patrick.";
        return;
    }
    
    request.open("GET", url, true);
    
    request.send(null);

    request.onreadystatechange = function ()
    {
        if (request.readyState == XMLHttpRequest.DONE)
        {
            if (request.status == 200)
            {
                var responseText = request.responseText  
                var word = JSON.parse(responseText)
                try 
                {
                    ws.value = word.wordSpelling
                    wd.value = word.wordDefinition
                    wg.value = word.wordGrammar
                    we.value = word.wordExample
                    wa.value = word.wordAttempts
                    wc.value = word.wordCorrect
                    ww.value = word.wordWrong
                    wp.value = word.wordPercentage
                    ms.value = ''
                    md.value = ''
                    st.value = "Next word was found."
                }
                catch(err) 
                {
                    st.value = "Error parsing response.  Check the log."
                    console.log(err)
                }    
            }
            else if (request.status = 404)
            {
                st.value = "Next word was not found." 
            }
            else
            {
                st.value = "Unsuccessful request:  " + request.readyState + "  " + request.status  + ".  Call Patrick."
            }
        }           
        return
    }
}