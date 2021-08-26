const puppeteer = require("puppeteer");
const readline = require("readline");
var fs = require("fs");
const url = "103.31.226.51:3000";

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

let datacenter;
const start = async () => {
  console.log("1. BLC Linux Full Monitor");
  console.log("2. Microgen Linux Full Monitor");
  console.log("3. P-Rancher Linux Monitoring Full");
  console.log("pilih mana? ");
  for await (const line of rl) {
    // console.log(line);
    datacenter = line - 1;
    rl.close();
  }
};

function delay(time) {
  return new Promise(function (resolve) {
    setTimeout(resolve, time);
  });
}

(async () => {
  await start();
  const browser = await puppeteer.launch({
    executablePath: "/usr/bin/google-chrome",
    headless: false,
    args: [
      "--no-sandbox",
      // "--user-data-dir=/home/bt66/belajar/chromedata",
      "--window-size=${options.width},${options.height}",
    ],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 1360 });
  await page.goto("https://monitoring.carakan.id", {
    waitUntil: "load",
    timeout: 0,
  });
  // await delay(3000);

  await page.type(".css-mtvhwr-input-input", "admin");
  const example = await page.$x(
    "/html/body/div/div/div[2]/div[3]/div/div[2]/div/div/form/div[2]/div[2]/div/div/input"
  );
  await example[0].type("2wsx1qaz");

  const form = await page.$(".css-w9m50q-button");
  await form.evaluate(
    (form) => {
      form.click();
    },
    { waitUntil: "load", timeout: 0 }
  );

  var selector = ".css-1kygs5l";
  await page.waitForSelector(selector);
  const dataCenter = await page.$$(".css-1kygs5l");

  console.log("datacenter ada :" + dataCenter);
  await dataCenter[datacenter].click();

  await delay(5000);

  let cpu_memory = await page.$x(
    "/html/body/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[2]/div[18]/div",
    { waitUntil: "load" }
  );

  await cpu_memory[0].click();

  let ip;
  let list_ip_address = await page.$x(
    "/html/body/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[1]/div/div[3]/div/div/a",
    { waitUntil: "load" }
  );
  await list_ip_address[0].click();

  const el = await page.$$(".variable-option.pointer");
  await console.log("list ip ada : " + el.length);

  var click_mbuh_nondi = ".gf-form-label.gf-form-label--variable";
  await page.waitForSelector(click_mbuh_nondi);
  await page.click(click_mbuh_nondi);

  let dir;
  for (let i = 1; i <= el.length; i++) {
    if (datacenter == 1) {
      dir = "./blc_full_monitoring";
      if (!fs.existsSync(dir)) {
        await fs.mkdirSync(dir);
      }
    } else if (datacenter == 2) {
      dir = "./microgen_full_monitoring";
      if (!fs.existsSync(dir)) {
        await fs.mkdirSync(dir);
      }
    } else {
      dir = "./project_rancher";
      if (!fs.existsSync(dir)) {
        await fs.mkdirSync(dir);
      }
    }
    await delay(2000);
    let ip_list = await page.$x(
      "/html/body/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[1]/div/div[3]/div/div/a",
      { waitUntil: "load" }
    );
    await ip_list[0].click();

    await delay(1000);

    ip = await page.$x(
      `/html/body/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[1]/div/div[3]/div/div/div/div/div/div/a[${i}]`,
      { waitUntil: "load" }
    );

    await ip[0].click();
    let ip_Server = await page.evaluate(
      () => document.querySelectorAll(".css-5t1gy9")[2].innerHTML
    );
    await page.screenshot({ path: `./${dir}/${ip_Server}.png` });
  }
})();
