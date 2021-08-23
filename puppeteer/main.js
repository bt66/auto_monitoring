const puppeteer = require("puppeteer");
// set your grafana here
const url = "";
// set your grafana username here
const username="";
// set your grafana password here
const password="";


(async () => {
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
  await page.setViewport({ width: 1280, height: 720 });
  await page.goto(url, {
    waitUntil: "load",
    timeout: 0,
  });
  // await delay(3000);

  await page.type(".css-mtvhwr-input-input", username);
  const example = await page.$x(
    "/html/body/div/div/div[2]/div[3]/div/div[2]/div/div/form/div[2]/div[2]/div/div/input"
  );
  await example[0].type(password);

  const form = await page.$(".css-w9m50q-button");
  await form.evaluate(
    (form) => {
      form.click();
    },
    { waitUntil: "load", timeout: 0 }
  );

  var selector = ".css-1kygs5l";
  await page.waitForSelector(selector);
  await page.click(selector);

  // click ip list
  // console.log(ip_list[0]);

  await page.screenshot({ path: "satu.png" });
  await delay(7000);
  // click cpu memory/ net /disk

  let cpu_memory = await page.$x(
    "/html/body/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[2]/div[18]/div",
    { waitUntil: "load" }
  );

  await cpu_memory[0].click();

  // const elements = await page.$$(".panel-container.panel-container--absolute");

  // for (let i = 0; i < elements.length; i++) {
  //   try {
  //     // get screenshot of a particular element
  //     await elements[i].screenshot({ path: `${i}.png` });
  //   } catch (e) {
  //     // if element is 'not visible', spit out error and continue
  //     console.log(
  //       `couldnt take screenshot of element with index: ${i}. cause: `,
  //       e
  //     );
  //   }
  // }

  let ip;
  for (let i = 1; i <= 26; i++) {
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
    await page.screenshot({ path: `${ip_Server}.png` });

    const elements = await page.$$(
      ".panel-container.panel-container--absolute"
    );

    for (let j = 15; j <= 16; j++) {
      try {
        // get screenshot of a particular element
        await elements[j].screenshot({ path: `${ip_Server} ${j}.png` });
      } catch (e) {
        // if element is 'not visible', spit out error and continue
        console.log(
          `couldnt take screenshot of element with index: ${i} ${j}. cause: `,
          e
        );
      }
    }
  }

  // /html/body/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[2]/div[13]/div

  // /html/body/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[2]/div[14]/div
  // // click ip list
  // await delay(1000);
  // ip_list = await page.$x(
  //   "/html/body/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[1]/div/div[3]/div/div/a",
  //   { waitUntil: "load" }
  // );
  // await ip_list[0].click();
  // // click ip ke 3

  // await delay(1000);
  // const ip_tiga = await page.$x(
  //   "/html/body/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[1]/div/div[3]/div/div/div/div/div/div/a[3]",
  //   { waitUntil: "load" }
  // );
  // await ip_tiga[0].click();
  // await page.screenshot({ path: "tiga.png" });

  // await delay(1000);
  // ip_list = await page.$x(
  //   "/html/body/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[1]/div/div[3]/div/div/a",
  //   { waitUntil: "load" }
  // );
  // await ip_list[0].click();
  // // click ip ke 3

  // await delay(1000);
  // const ip_tiga = await page.$x(
  //   "/html/body/div/div/div[2]/div[3]/div[2]/div/div[1]/div/div[1]/div/div[3]/div/div/div/div/div/div/a[3]",
  //   { waitUntil: "load" }
  // );
  // await ip_tiga[0].click();
  // await page.screenshot({ path: "tiga.png" });
})();
