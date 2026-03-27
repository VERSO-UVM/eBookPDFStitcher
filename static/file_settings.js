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

    // get all the user's files
    async function getInputList() {
        // call flask thing to retrieve all uploaded files
        response = await fetch('/getInputList');
        files = await response.json();
        
        const list = document.getElementById("pdf-list")
        // add each pdf to the DOM
        for(const file of files) {
            console.log(file);
            const li = document.createElement("li");
            li.setAttribute("class","pdf-li");
            
            const details = document.createElement("details");
            const summary = document.createElement("summary");
            const title = document.createElement("span")
            title.setAttribute("class","pdf-title")
            title.innerText = file.title
            summary.appendChild(title)

            details.appendChild(summary);
            
            // dropdown with individual pages list (for more granular reordering/deleting in the future.)
            const nested_ul = document.createElement("ol");
            nested_ul.setAttribute("class","nested-ol");
            for (i = 1; i<=file.numPages;i++) {
                const nested_li = document.createElement("li");
                nested_li.setAttribute("class","nested-li")
                const page_num = document.createElement("p");
                page_num.innerText = i

                const checkbox = document.createElement("input");
                checkbox.setAttribute("type","checkbox");

                nested_li.appendChild(page_num);
                nested_li.appendChild(checkbox);
                nested_ul.appendChild(nested_li);
            }
            details.append(nested_ul);
            const numpg = document.createElement("span")
            numpg.setAttribute("class","page-num")
            numpg.innerText = file.numPages
            summary.append(numpg)
            li.appendChild(details);
            list.appendChild(li);
        }
    }

    getInputList();

    // this can be called at any point automatically to reload the pdf!!
    reloadPDFViewer(`/files/stitched_pdfs/auto_stitched.pdf`);


    
};
