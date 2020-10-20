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

if (config.runsInWidget) {
	
  var widgetInputRAW = args.widgetParameter
  try {
    widgetInputRAW.toString()
  } catch(e) {
  // 默认值
    widgetInputRAW = "sz000001"
  }
  // 初始化股票ID
  var fid = widgetInputRAW.toString().split(",")	
	

	  // 获取股票数据
	const fundJSON = await getFund()
  
	// 创建小组件
	const widget = createWidget(fundJSON)
	widget.addSpacer()
	widget.setPadding(15, 2, 15, 2)
	widget.backgroundImage = widget.backgroundImage
	Script.setWidget(widget)
	Script.complete()

//


/*
 * 以下函数定义
 */

 // 股票数据获取
async function getFund() {
  // 拼接股票id
  var fidFull = ''
  for (let index in fid) {
    fidFull = fidFull + fid[index] + ","
  }
  fidFull = fidFull.substring(0, fidFull.lastIndexOf(','))

  // 请求股票数据
  const fundRequest = {
    url: `https://api.doctorxiong.club/v1/stock?code=${fidFull}`,
  }
  const res = await get(fundRequest)

  return res
}

// 创建 widget
function createWidget(fundJson) {
  let listWidget = new ListWidget() 
  listWidget.backgroundImage = files.readImage(path)
  // 下面是设置纯色背景
  //const bgColor = new LinearGradient()
  //bgColor.colors = [new Color("#29323c"), new Color("#1c1c1c")]
  //bgColor.locations = [0.0, 1.0]
  //listWidget.backgroundGradient = bgColor

  const data = fundJSON.data
  for (let index in data) {
    // 添加行距
    listWidget.addSpacer(4)
    // 统一字体大小
    const fontSize = 11

    //创建水平方向stack
    let hStack0 = listWidget.addStack()
    hStack0.layoutHorizontally()
    hStack0.addSpacer(0) // Left spacing, 向左对齐间距

    // 颜色值
    const priceChange = data[index].priceChange // 当前涨幅
    var color = new Color('dc0000')
    if (priceChange <= 0) {
      color = new Color('097C25')
    }

	let priceStr = data[index].price
	let priceCha = data[index].changePercent
	
    // 股票名称
   let title = hStack0.addText(data[index].name +' 价:' + priceStr + ' 涨:' + priceChange +' 幅:' + priceCha)
    title.font = new Font('Menlo', fontSize) //font and size,字体与大小
    title.textColor = color //font color,字体颜色
    title.textOpacity = (1) //opacity,不透明度
    title.leftAlignText() //Align,对齐方式(center,left,right)！在同一个stack内的对齐方式不能单独设置，只能调整向左对齐间距大小 
    

    // 净值估算更新日期 
    let Pricedate = data[index].date.substring(11, 19)
    let expectWorthDate = hStack0.addText(' 更:'+ Pricedate + '')
    expectWorthDate.font = new Font('Menlo', fontSize) //font and size,字体与大小
    expectWorthDate.textColor = color //font color,字体颜色
    expectWorthDate.textOpacity = (1) //opacity,不透明度
    expectWorthDate.leftAlignText() //Align,对齐方式(center,left,right)！在同一个stack内的对齐方式不能单独设置，只能调整向左对齐间距大小 
  }

  return listWidget
}

// 网络请求get封装
async function get({ url, headers = {} }, callback = () => {}) {
  const request = new Request('')
  const defaultHeaders = {
    "Accept": "*/*",
    "Content-Type": "application/json"
  }

  request.url = url
  request.method = 'GET'
  request.headers = {
    ...headers,
    ...defaultHeaders
  }
  const data = await request.loadJSON()
  callback(request.response, data)
  return data
}
//

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