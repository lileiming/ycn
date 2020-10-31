// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: orange; icon-glyph: magic;
// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: deep-purple; icon-glyph: image;

// This widget was created by Max Zeryck @mzeryck

// Widgets are unique based on the name of the script.



const filename = Script.name() + ".jpg"
const files = FileManager.local()
const path = files.joinPath(files.documentsDirectory(), filename)
let widgetHello = new ListWidget(); 
var today = new Date();

var widgetInputRAW = args.widgetParameter;

try {
    widgetInputRAW.toString();
} catch(e) {
    widgetInputRAW = "50|#f0f8ff";
}

var widgetInput = widgetInputRAW.toString();

var inputArr = widgetInput.split("|");

// iCloud file path
var scriptableFilePath = "/var/mobile/Library/Mobile Documents/iCloud~dk~simonbs~Scriptable/Documents/";
var removeSpaces1 = inputArr[0].split(" "); // Remove spaces from file name
var removeSpaces2 = removeSpaces1.join('');
var tempPath = removeSpaces2.split(".");
var backgroundImageURLRAW = scriptableFilePath + tempPath[0];

var fm = FileManager.iCloud();
var backgroundImageURL = scriptableFilePath + tempPath[0] + ".";
var backgroundImageURLInput = scriptableFilePath + removeSpaces2;

// For users having trouble with extensions
// Uses user-input file path is the file is found
// Checks for common file format extensions if the file is not found
if (fm.fileExists(backgroundImageURLInput) == false) {
        var fileTypes = ['png', 'jpg', 'jpeg', 'tiff', 'webp', 'gif'];

        fileTypes.forEach(function(item) {
            if (fm.fileExists((backgroundImageURL + item.toLowerCase())) == true) {
                backgroundImageURL = backgroundImageURLRAW + "." + item.toLowerCase();
            } else if (fm.fileExists((backgroundImageURL + item.toUpperCase())) == true) {
                backgroundImageURL = backgroundImageURLRAW + "." + item.toUpperCase();
            }
        });
} else {
    backgroundImageURL = scriptableFilePath + removeSpaces2;
}

var spacing = parseInt(inputArr[1]);

//API_KEY
let API_WEATHER = "12b2817fbec86915a6e9b4dbbd3d9036";//Load Your api here
let CITY_WEATHER = "1790630";//add your city ID

//Get storage
var base_path = "/var/mobile/Library/Mobile Documents/iCloud~dk~simonbs~Scriptable/Documents/weather/";
var fm = FileManager.iCloud();

// Fetch Image from Url
async function fetchimageurl(url) {
    const request = new Request(url)
    var res = await request.loadImage();
    return res;
}

// Get formatted Date
function getformatteddate(){
  var months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  return months[today.getMonth()] + " " + today.getDate()
}

// Long-form days and months
var days = ['周日','周一','周二','周三','周四','周五','周六'];
var months = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'];

// Load image from local drive
async function fetchimagelocal(path){
  var finalPath = base_path + path + ".png";
  if(fm.fileExists(finalPath)==true){
    console.log("file exists: " + finalPath);
    return finalPath;
  }else{
    //throw new Error("Error file not found: " + path);
    if(fm.fileExists(base_path)==false){
      console.log("Directry not exist creating one.");
      fm.createDirectory(base_path);
    }
    console.log("Downloading file: " + finalPath);
    await downloadimg(path);
    if(fm.fileExists(finalPath)==true){
      console.log("file exists after download: " + finalPath);
      return finalPath;
    }else{
      throw new Error("Error file not found: " + path);
    }
  }
}

async function downloadimg(path){
    const url = "http://a.animedlweb.ga/weather/weathers25_2.json";
    const data = await fetchWeatherData(url);
    var dataimg = null;
    var name = null;
    if(path.includes("bg")){
      dataimg = data.background;
      name = path.replace("_bg","");
    }else{
      dataimg = data.icon;
      name = path.replace("_ico","");
    }
    var imgurl=null;
    switch (name){
      case "01d":
        imgurl = dataimg._01d;
      break;
      case "01n":
        imgurl = dataimg._01n;
      break;
      case "02d":
        imgurl = dataimg._02d;
      break;
      case "02n":
        imgurl = dataimg._02n;
      break;
      case "03d":
        imgurl = dataimg._03d;
      break;
      case "03n":
        imgurl = dataimg._03n;
      break;
      case "04d":
        imgurl = dataimg._04d;
      break;
      case "04n":
        imgurl = dataimg._04n;
      break;
      case "09d":
        imgurl = dataimg._09d;
      break;
      case "09n":
        imgurl = dataimg._09n;
      break;
      case "10d":
        imgurl = dataimg._10d;
      break;
      case "10n":
        imgurl = dataimg._10n;
      break;
      case "11d":
        imgurl = dataimg._11d;
      break;
      case "11n":
        imgurl = dataimg._11n;
      break;
      case "13d":
        imgurl = dataimg._13d;
      break;
      case "13n":
        imgurl = dataimg._13n;
      break;
      case "50d":
        imgurl = dataimg._50d;
      break;
      case "50n":
        imgurl = dataimg._50n;
      break;
    }
    const image = await fetchimageurl(imgurl);
    console.log("Downloaded Image");
    fm.writeImage(base_path+path+".png",image);
}

//get Json weather
async function fetchWeatherData(url) {
  const request = new Request(url);
  const res = await request.loadJSON();
  return res;
}

// Get Location 
/*Location.setAccuracyToBest();
let curLocation = await Location.current();
console.log(curLocation.latitude);
console.log(curLocation.longitude);*/
let wetherurl = "http://api.openweathermap.org/data/2.5/weather?id=" + CITY_WEATHER + "&APPID=" + API_WEATHER + "&units=metric";

const weatherJSON = await fetchWeatherData(wetherurl);
const cityName = weatherJSON.name;
const weatherarry = weatherJSON.weather;
const iconData = weatherarry[0].icon;
const weathername = weatherarry[0].main;
const curTempObj = weatherJSON.main;
const curTemp = curTempObj.temp;
const highTemp = curTempObj.temp_max;
const lowTemp = curTempObj.temp_min;
const feel_like = curTempObj.feels_like;
//Completed loading weather data

// Greetings arrays per time period. 
var greetingsMorning = [
'星宝爹，早上要专心'
];
var greetingsNoon = [
'星宝爹，中午瞌睡吧'
];
var greetingsAfternoon = [
'星宝爹，下午少吃点'
];
var greetingsEvening = [
'星宝爹，明天咱干啥'
];
var greetingsNight = [
'星宝爹，你就不要睡'
];
var greetingsLateNight = [
'你就不要睡觉，睡觉浪费时间！'
];


// Holiday customization
var holidaysByKey = {
    // month,week,day: datetext
    "11,4,4": "Happy Thanksgiving!"
}

var holidaysByDate = {
    // month,date: greeting
    "1,1": "Happy " + (today.getFullYear()).toString() + "!",
    "10,31": "Happy Halloween!",
    "12,25": "Merry Christmas!"
}

var holidayKey = (today.getMonth() + 1).toString() + "," +  (Math.ceil(today.getDate() / 7)).toString() + "," + (today.getDay()).toString();

var holidayKeyDate = (today.getMonth() + 1).toString() + "," + (today.getDate()).toString();

// Date Calculations
var weekday = days[ today.getDay() ];
var month = months[ today.getMonth() ];
var date = today.getDate();
var hour = today.getHours();

//Work time  Render
function renderWorkProgress() {
    const now = new Date()
    const nowHour = now.getHours()
    const nowMin = now.getMinutes()
    const nowTime = nowHour * 3600 + nowMin * 60
    const start = 31500// Start of this year
    const end = 63000// End of this year
//     var progress = 0
    var progress = (nowTime - start) / (end - start)
    if (nowTime >= end){
       progress = 1}
    if (nowTime < start){
       progress = 0}
    
    return renderWProgress(progress)
  }
  
  function renderWProgress(progress) {
    const used = '▓'.repeat(Math.floor(progress * 20))
    const left = '░'.repeat(20 - used.length)
    var txt = '上班中……'
    if(progress >= 1 ){
      txt ='下班啦……'
    }
     if(progress == 0 ){
      txt ='快上班啦……'
    }
    return `${used}${left} ${Math.floor(progress * 100)}% ${txt}`
  }


// Append ordinal suffix to date
function ordinalSuffix(input) {
    if (input % 10 == 1 && date != 11) {
        return input.toString() + "日";
    } else if (input % 10 == 2 && date != 12) {
        return input.toString() + "日";
    } else if (input % 10 == 3 && date != 13) {
        return input.toString() + "日";
    } else {
        return input.toString() + "日";
    }
}

// Generate date string
var datefull = month + " " + ordinalSuffix(date) +", " + weekday;

// Support for multiple greetings per time period
function randomGreeting(greetingArray) {
    return Math.floor(Math.random() * greetingArray.length);
}

var greeting = new String("Howdy.")
if (hour < 5 && hour >= 1) { // 1am - 5am
    greeting = greetingsLateNight[randomGreeting(greetingsLateNight)];
} else if (hour >= 23 || hour < 1) { // 11pm - 1am
    greeting = greetingsNight[randomGreeting(greetingsNight)];
} else if (hour <= 11) { // Before noon (5am - 12pm)
    greeting = greetingsMorning[randomGreeting(greetingsMorning)];
} else if (hour >11 && hour <= 13)  { // 11am - 1pm
    greeting = greetingsNoon[randomGreeting(greetingsNoon)];
} else if (hour > 13 && hour <= 19) { // 1pm - 5pm
    greeting = greetingsAfternoon[randomGreeting(greetingsAfternoon)];
} else if (hour > 19 && hour < 23) { // 5pm - 11pm
    greeting = greetingsEvening[randomGreeting(greetingsEvening)];
} 

// Overwrite greeting if calculated holiday
if (holidaysByKey[holidayKey]) {
    greeting = holidaysByKey[holidayKey];
}

// Overwrite all greetings if specific holiday
if (holidaysByDate[holidayKeyDate]) {
    greeting = holidaysByDate[holidayKeyDate];
}

//Battery Render
function getBatteryLevel() {
    const batteryLevel = Device.batteryLevel()
    const batteryAscii = Math.round(batteryLevel * 100);
    return batteryAscii + "%";
}


// Try/catch for color input parameter
try {
    inputArr[0].toString();
} catch(e) {
    throw new Error("Please long press the widget and add a parameter.");
}

let themeColor = new Color(inputArr[0].toString());


if (config.runsInWidget) {
  let widget = new ListWidget()
  widget.backgroundImage = files.readImage(path)
  
 // You can your own code here to add additional items to the "invisible" background of the widget.
 /* --------------- */
 /* Assemble Widget */
 /* --------------- */
 
 
 //Top spacing
 widgetHello.addSpacer(15);

 // Greeting label
 let hello = widgetHello.addText(greeting);
 hello.font = Font.boldSystemFont(35);
 hello.textColor = new Color('#f0f8ff');
 hello.leftAlignText();
 
//Spacing between greeting and yearprogress
widgetHello.addSpacer(5);

//define horizontal stack
let hStack0 = widgetHello.addStack();
hStack0.layoutHorizontally();

// Centers date line
hStack0.addSpacer(0)

// Year icon in stack
const YearProgressicon = hStack0.addText("◕ ")
YearProgressicon.font = new Font('Menlo', 12)
YearProgressicon.textColor = new Color('#f0f8ff')
YearProgressicon.textOpacity = (1);
YearProgressicon.leftAlignText();

// Year label in stack
const YearProgress = hStack0.addText("上班 "+renderWorkProgress())
YearProgress.font = new Font('Menlo', 12)
YearProgress.textColor = new Color('#f0f8ff')
 YearProgress.textOpacity = (1);
YearProgress.leftAlignText();

//Spacing between yearprogress and battery
widgetHello.addSpacer(5);

//define horizontal stack
let hStack1 = widgetHello.addStack();
hStack1.layoutHorizontally();

// Centers date line
hStack1.addSpacer(0)

// Battery icon in stack 
const batteryicon = hStack1.addText("⚡ 电能");
batteryicon.textColor = new Color("#f0f8ff"); 
batteryicon.font = new Font('Menlo', 12); 
batteryicon.leftAlignText();

// Battery Progress in stack 
const batteryLine = hStack1.addText(renderBattery());
batteryLine.textColor = new Color("#f0f8ff"); 
batteryLine.font = new Font("Menlo", 12); 
batteryLine.leftAlignText();
function renderBattery() { 
const batteryLevel = Device.batteryLevel(); 
const juice = "▓".repeat(Math.floor(batteryLevel * 10)); 
const used = "░".repeat(10 - juice.length) 
const batteryAscii = " " + juice + used + " " ; 
return batteryAscii; }

// Battery Status in stack
var battery =  getBatteryLevel();
var batcolor = new Color('#097C25')
if(Device.isCharging() && !Device.isFullyCharged()){
  battery = battery + " , 充电中...";
  batcolor = new Color('#dc0000')
}

if(Device.isFullyCharged()){
  battery = battery + " , 已充满电!请拔下电源!";
  batcolor = new Color('#ff00ff')
}
let batterytext = hStack1.addText(battery);
batterytext.font = new Font("Menlo", 12);
batterytext.textColor = batcolor;

//Spacing between battery and summary
widgetHello.addSpacer(5);

// Widget feel temp
let feel = cityName + "天气：" + weathername + "." + " 最低温度: " + Math.round(lowTemp) + "\u2103" + ";" + " 最高温度: " + Math.round(highTemp) + "\u2103";//"H:"+highTemp+"\u00B0"+" L:"+lowTemp+"\u00B0"
var hltemptext = widgetHello.addText(feel);
hltemptext.textColor = new Color('#f0f8ff');
hltemptext.font = Font.regularSystemFont(12);
hltemptext.leftAlignText();
hltemptext.textOpacity = (0.7);

//define horizontal stack
let hStack2 = widgetHello.addStack();
hStack2.layoutHorizontally();

// Centers weather line
hStack2.addSpacer(0)

// Date label
const datetext = hStack2.addText(datefull + "  ");
datetext.font = Font.regularSystemFont(30);
datetext.textColor = new Color('#f0f8ff');
datetext.textOpacity = (1);
datetext.leftAlignText();

//image
var img = Image.fromFile(await fetchimagelocal(iconData + "_ico"));
 
//image in stack
let widgetimg = hStack2.addImage(img);
widgetimg.imageSize = new Size(40, 40);
widgetimg.leftAlignImage();

//tempeture label in stack
let temptext = hStack2.addText('\xa0\xa0'+  Math.round(feel_like).toString()+"\u2103");
temptext.font = Font.boldSystemFont(30);
temptext.textColor = new Color('#f0f8ff');
//temptext.textOpacity = (0.5);
temptext.leftAlignText();

// Bottom Spacer
 widgetHello.addSpacer();
 widgetHello.setPadding( 0, 0, 0, 0)
 widgetHello.backgroundImage = widget.backgroundImage
  Script.setWidget(widgetHello)
  Script.complete()


/*
 * The code below this comment is used to set up the invisible widget.
 * ===================================================================
 */
} else {
  
  // Determine if user has taken the screenshot.
  var message
  message = "开始之前，请返回主屏幕并长按进入编辑模式。滑动到最右边的空白页并截图。"
  let exitOptions = ["继续","退出以截图"]
  let shouldExit = await generateAlert(message,exitOptions)
  if (shouldExit) return
  
  // Get screenshot and determine phone size.
  let img = await Photos.fromLibrary()
  let height = img.size.height
  let phone = phoneSizes()[height]
  if (!phone) {
    message = "您似乎选择了非iPhone屏幕截图的图像，或者不支持您的iPhone。请使用其他图像再试一次。"
    await generateAlert(message,["OK"])
    return
  }
  
  // Prompt for widget size and position.
  message = "您想要创建什么尺寸的小部件？"
  let sizes = ["Small","Medium","Large"]
  let size = await generateAlert(message,sizes)
  let widgetSize = sizes[size]
  
  message = "您想它在什么位置？"
  message += (height == 1136 ? " (请注意，您的设备仅支持两行小部件，因此中间和底部选项相同。)" : "")
  
  // Determine image crop based on phone size.
  let crop = { w: "", h: "", x: "", y: "" }
  if (widgetSize == "Small") {
    crop.w = phone.small
    crop.h = phone.small
    let positions = ["Top left","Top right","Middle left","Middle right","Bottom left","Bottom right"]
    let position = await generateAlert(message,positions)
    
    // Convert the two words into two keys for the phone size dictionary.
    let keys = positions[position].toLowerCase().split(' ')
    crop.y = phone[keys[0]]
    crop.x = phone[keys[1]]
    
  } else if (widgetSize == "Medium") {
    crop.w = phone.medium
    crop.h = phone.small
    
    // Medium and large widgets have a fixed x-value.
    crop.x = phone.left
    let positions = ["Top","Middle","Bottom"]
    let position = await generateAlert(message,positions)
    let key = positions[position].toLowerCase()
    crop.y = phone[key]
    
  } else if(widgetSize == "Large") {
    crop.w = phone.medium
    crop.h = phone.large
    crop.x = phone.left
    let positions = ["Top","Bottom"]
    let position = await generateAlert(message,positions)
    
    // Large widgets at the bottom have the "middle" y-value.
    crop.y = position ? phone.middle : phone.top
  }
  
  // Crop image and finalize the widget.
  let imgCrop = cropImage(img, new Rect(crop.x,crop.y,crop.w,crop.h))
  
  message = "您的小部件背景已准备就绪。您想在Scriptable的小部件中使用它还是导出图像？"
  const exportPhotoOptions = ["在Scriptable中使用","导出图像"]
  const exportPhoto = await generateAlert(message,exportPhotoOptions)
  
  if (exportPhoto) {
    Photos.save(imgCrop)
  } else {
    files.writeImage(path,imgCrop)
  }
  
  Script.complete()
}

// Generate an alert with the provided array of options.
async function generateAlert(message,options) {
  
  let alert = new Alert()
  alert.message = message
  
  for (const option of options) {
    alert.addAction(option)
  }
  
  let response = await alert.presentAlert()
  return response
}

// Crop an image into the specified rect.
function cropImage(img,rect) {
   
  let draw = new DrawContext()
  draw.size = new Size(rect.width, rect.height)
  
  draw.drawImageAtPoint(img,new Point(-rect.x, -rect.y))  
  return draw.getImage()
}

// Pixel sizes and positions for widgets on all supported phones.
function phoneSizes() {
  let phones = { 
 "2688": {
   "small":  507,
   "medium": 1080,
   "large":  1137,
   "left":  81,
   "right": 654,
   "top":    228,
   "middle": 858,
   "bottom": 1488
 },
 
 "1792": {
   "small":  338,
   "medium": 720,
   "large":  758,
   "left":  54,
   "right": 436,
   "top":    160,
   "middle": 580,
   "bottom": 1000
 },
 
 "2436": {
   "small":  465,
   "medium": 987,
   "large":  1035,
   "left":  69,
   "right": 591,
   "top":    213,
   "middle": 783,
   "bottom": 1353
 },
 
 "2208": {
   "small":  471,
   "medium": 1044,
   "large":  1071,
   "left":  99,
   "right": 672,
   "top":    114,
   "middle": 696,
   "bottom": 1278
 },
 
 "1334": {
   "small":  296,
   "medium": 642,
   "large":  648,
   "left":  54,
   "right": 400,
   "top":    60,
   "middle": 412,
   "bottom": 764
 },
 
 "1136": {
   "small":  282,
   "medium": 584,
   "large":  622,
   "left": 30,
   "right": 332,
   "top":  59,
   "middle": 399,
   "bottom": 399
 }
  }
  return phones
}
