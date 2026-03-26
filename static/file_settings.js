window.onload = function () {
    const form = document.getElementById("choosing_a_name");
    const button = document.getElementById("changing_form");
    const para = document.getElementById("changing_title");
    const forbiden_input = /[\\\/\:\*\?\"\<\>\|]/;

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const file_name = document.getElementById("file_name").value.trim();
        if (forbiden_input.test(file_name)) {
            alert('You have entered a forbidden input. \nForbiden input are : \\ , / , : , * , ? , " , < , > , | ')
        }
        else {
            form.innerHTML = "<br>"
            para.innerHTML = `You have chosen the name '${file_name}' — feel free to click the button below to download your final result`;
            button.innerHTML = `
                <form action="/file_settings" method='POST'>
                    <input type='hidden' name='file_name' value='${file_name}'>
                    <button type='submit' name='action' value='stitch'>Download PDF</button>
                </form>`;
        }
    });

    async function reloadPDFViewer(src) {
        const { default: EmbedPDF } = await import('https://cdn.jsdelivr.net/npm/@embedpdf/snippet@2/dist/embedpdf.js');

        const container = document.getElementById('pdf-viewer');
        container.innerHTML = '';

        const viewer = EmbedPDF.init({
            type: 'container',
            target: container,
            src
        });
        return viewer;
    }

    // this can be called at any point automatically to reload the pdf!!
    reloadPDFViewer(`/files/stitched_pdfs/auto_stitched.pdf`);
};

