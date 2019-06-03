function addWord()
{
    wa.value = "0";
    wc.value = "0";
    ww.value = "0";
    wp.value = "0.0";

    st.value = "Adding word.  Please wait."; 

    // If the browser does not support the XMLHttpRequest object, do nothing.
    if (!window.XMLHttpRequest)
    {
        st.value = "window.XMLHttpRequest failed.  Call Patrick.";
        return;
    }
    
    var wordSpelling = ws.value;
    
    if (!wordSpelling) 
    {
        st.value = "Spelling is required.";
        return;
    }
    
    var wordDefinition = wd.value;
    
    if (!wordDefinition) 
    {
        st.value = "Definition is required.";
        return;
    }
    
    var wordGrammar = wg.value;
    
    if (!wordGrammar) 
    {
        st.value = "Grammar is required.";
        return;
    }
    
    var wordExample = we.value;
    
    if (!wordExample) 
    {
        st.value = "Example is required.";
        return;
    }

    // Create the word dictionary.
    word = {}
    word["wordSpelling"] = wordSpelling
    word["wordGrammar"] = wordGrammar
    word["wordDefinition"] = wordDefinition
    word["wordExample"] = wordExample
    word["wordAttempts"] = 0
    word["wordCorrect"] = 0
    word["wordWrong"] = 0
    word["wordPercentage"] = 0.0

    // Convert the word from a dictionary to a JSON string.
    word = JSON.stringify(word)
    
    // Encode the user input as query parameters in a URL.
    var hostAndPort = location.host; 
    if (hostAndPort == '127.0.0.1:5000')
    {
        url = "http://" + hostAndPort + "/add_word"
    }
    else
    {
        url = "https://" + hostAndPort + "/add_word" 
    }
    
    // Fetch the contents of that URL using the XMLHttpRequest object.
    var request = new XMLHttpRequest();
    
    if (!request)
    {
        st.value = "new XMLHttpRequest() returned null.  Call Patrick.";
        return;
    }
    
    request.open("POST", url, true);
    
    request.setRequestHeader("content-type", "application/json");
    
    request.send(word)
    
    request.onreadystatechange = function ()
    {        
        if (request.readyState == XMLHttpRequest.DONE)
        {
            if (request.status == 200)
            {            
                st.value = 'Word was added.'
            }
            else if (request.status == 404)
            {            
                st.value = 'Word was not found.'
            }
            else
            {
                st.value = "Unsuccessful request:  " + request.readyState + "  " + request.status;
            }
        }
        return
    }
}