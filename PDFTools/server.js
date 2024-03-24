import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import multer from 'multer';
import mergePDFs from './mergePDF.js';

const upload = multer({ dest: 'uploads/' });
const app = express();
const port = 3000;

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

app.use('/static', express.static('public'));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
})

app.post('/merge', upload.array('pdfs', 20), async (req, res, next) => {

    if (!req.files || req.files.length < 2) {
        return res.status(400).send('Please upload at least 2 PDF files');
    }

    let mergedFilePaths = [];
    for (let file of req.files) {
        mergedFilePaths.push(path.join(__dirname, file.path));
    }

    let mergedFileName = await mergePDFs(mergedFilePaths);
    res.redirect(`http://localhost:${port}/static/${mergedFileName}`);
})

app.listen(port, () => {
  console.log(`Example app listening on port http://localhost:${port}`);
})