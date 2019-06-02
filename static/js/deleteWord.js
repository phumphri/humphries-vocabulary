function deleteWord()
{

    console.log('deleteWord() was called.')

    st.value = "Deleting word.  Please wait."; 

    // If the browser does not support the XMLHttpRequest object, do nothing.
    if (!window.XMLHttpRequest)
    {
        st.value = "window.XMLHttpRequest failed.  Call Patrick.";
        return
    }
    
    // Encode the user input as query parameters in a URL.
    var hostAndPort = location.host
    var url = "http://" + hostAndPort +"/delete_word/" + ws.value;
    
    // Fetch the contents of that URL using the XMLHttpRequest object.
    var request = new XMLHttpRequest();
    
    if (!request)
    {
        st.value = "new XMLHttpRequest() returned null.  Call Patrick.";
        return
    }
    
    request.open("GET", url, true);
    
    request.send(null)

    request.onreadystatechange = function ()
    {        
        if (request.readyState == XMLHttpRequest.DONE)
        {
            if (request.status == 200)
            {            
                st.value = 'Word was deleted.'
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