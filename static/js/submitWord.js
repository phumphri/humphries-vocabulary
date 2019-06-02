function submitTransaction()
{
    st.value = "Submitting Transaction.  Please wait.";
    //
    // If the browser does not support the XMLHttpRequest object, do nothing.
    if (!window.XMLHttpRequest)
    {
        st.value = "This browser does not support AJAX.  Try another.";
        return;
    }
    //   
    // Encode the user input as query parameters in a URL.
    var hostAndPort = location.host;
    var url = "http://" + hostAndPort + "/Transactions12/resources/transactions/merge";
    //
    // Fetch the contents of that URL using the XMLHttpRequest object.
    var request = new XMLHttpRequest();
    if (!request)
    {
        st.value = "new XMLHttpRequest() returned null.  Call Patrick.";
        return;
    }
    //
    var typeName = "Void";
    switch (tc.value)
    {
        case "C":
            typeName = "Credit";
            break;
        case "D":
            typeName = "Debit";
            break;
        case "X":
            typeName = "Deleted";
            break;
        case "V":
            typeName = "Void";
            break;
        default :
            typeName = "Unknown";
            break;
    }
    //
    try 
    {
        var string = "{";
        string += "\"transactionKey\":" + tk.value;
        //
        string += ", \"accountCode\" : \"" + ac.value + "\"";
        string += ", \"accountName\" : \"" + an.value + "\"";
        //
        string += ", \"typeCode\" : \"" + tc.value + "\"";
        string += ", \"typeName\" : \"" + typeName + "\"";
        //
        string += ", \"addressLine1\" : \"" + a1.value + "\"";
        string += ", \"addressLine2\" : \"" + a2.value + "\"";
        string += ", \"addressLine3\" : \"" + a3.value + "\"";
        string += ", \"addressLine4\" : \"" + a4.value + "\"";
        string += ", \"addressLine5\" : \"" + a5.value + "\"";
        //
        string += ", \"transactionAmount\" : " + ta.value + "  ";
        string += ", \"transactionBalance\" :0.00  ";
        //
        var transactionDate = new Date(cd.value);
        string += ", \"transactionDate\" :" + transactionDate.getTime();
        //
        string += ", \"checkNumber\" : \"" + cn.value + "\"";
        string += ", \"memo\" : \"" + tm.value + "\"";
        string += ", \"payeeName\" : \"" + pn.value + "\"";
        //
        var postDate = new Date(pd.value);
        string += ", \"postDate\" :" + postDate.getTime();
        string += "}";
    }
    catch (e)
    {
        st.value = "jsonObject build returned an Error:  " + e.toString();
        return;
    }
    //
    request.onreadystatechange = function ()
    {
        if (request.readyState == XMLHttpRequest.DONE && request.status == 204)
        {
            balanceTransactions();
            return;
        }

        if (request.readyState == XMLHttpRequest.UNSENT)
        {
            return;

        }
        if (request.readyState == XMLHttpRequest.OPENED)
        {
            return;
        }

        if (request.readyState == XMLHttpRequest.HEADERS_RECEIVED)
        {
            return;
        }

        if (request.readyState == XMLHttpRequest.LOADING)
        {
            return;
        }

        st.value = "Unsuccessful Transaction update:  " + request.readyState + "  " + request.status + ".  Call Patrick.";
    }
    //
    request.open("POST", url, true);
    //
    request.setRequestHeader("content-type", "text/plain");
    //
    request.send(string);
}   