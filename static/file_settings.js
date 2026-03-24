window.onload = function () {
    const form = document.getElementById("choosing_a_name");
    const button = this.document.getElementById("changing_form")
    forbiden_input = /[\\\/\:\*\?\"\<\>\|]/;
    

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const file_name = document.getElementById("file_name").value.trim(); 
        if(forbiden_input.test(file_name)){
            alert('You have entered a forbidden input. \nForbiden input are : \\ , / , : , * , ? , " , < , > , | ')
        }
        else{
            const username = document.getElementById("file_name").value.trim();
            //TODO pass this on to the flask, otherwise it is useless
            console.log(username);
            form.innerHTML ="<br>"
            button.innerHTML = " <form action='/file_settings' method='POST'> <button type='submit' name='action' value='stitch'>Stitch PDF</button> </form>";
        }

    });
};