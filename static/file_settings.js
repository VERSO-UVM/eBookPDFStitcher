window.onload = function () {
    const form = document.getElementById("choosing_a_name");
    const button = document.getElementById("changing_form")
    const para = document.getElementById("changing_title")
    forbiden_input = /[\\\/\:\*\?\"\<\>\|]/;


    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const file_name = document.getElementById("file_name").value.trim();
        if (forbiden_input.test(file_name)) {
            alert('You have entered a forbidden input. \nForbiden input are : \\ , / , : , * , ? , " , < , > , | ')
        }
        else {
            form.innerHTML = "<br>"
            para.innerHTML = `<p>You have chosen the name '${file_name}' feel free to click the button below to download your final result </p>`;
            button.innerHTML = `
                <form action="/file_settings" method='POST'>
                    <input type='hidden' name='file_name' value='${file_name}'>
                    <button type='submit' name='action' value='stitch'>Stitch PDF</button>
                </form>`;

        }});
};