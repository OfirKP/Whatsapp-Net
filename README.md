# Whatsapp Net
This project creates a network graph of connections out of your WhatsApp groups' participants data. 


<img align="center" src="https://i.imgur.com/oHtWhDC.png" width="600">

## Prerequisites
Make sure you have installed all of the following prerequisites on your machine:
- Node.js -  [Download & Install Node.js](https://nodejs.org/en/download/) and the _**npm**_ package manager.
- _python 3.7+_ (may work on older versions)

## Downloading & Installing
1. Clone this project
  ```bash
  $ git clone https://github.com/OfirKP/Whatsapp-Net
  ```
2. In the application directory (`$ cd Whatsapp-Net`), run this command:
  ```bash
  $ npm install
  ```
3. Install required python packages either by using `requirements.txt`:
```bash
$ pip install -r requirements.txt
```
_**or**_ by installing them directly:

```bash
$ pip install networkx==2.3 tqdm==4.32.1 matplotlib==3.1.1
```
## Usage

### Scraping
To generate a _json_ file with your groups' data, run the following command:
```bash
$ node scrape.js
```
A browser window should open. If you're not connected to WhatsApp web, connect by scanning QR code.

Wait until json file starts downloading.

### Generating Graph (GEXF file)
Edit `GROUPS_DATA_PATH` and `OUTPUT_GEXF_PATH` to match the location of the json input data and desired output location (custom command line arguments will be supported soon).

Then, run the python script:
```bash
$ python generate_graph.py
```

## Visualizing data
_**RECOMMENDED:**_ use a software like [Gephi](https://gephi.org/) that allows graph visualization, taking GEXF files as input.

## 💻 Technologies Used
* [Node](https://nodejs.org/en/)
* [puppeteer](https://github.com/GoogleChrome/puppeteer)
* [python 3.7](https://www.python.org/)

## License
This project is licensed under the GNU General Public License v2.0 . See [License](LICENSE) for more info.
