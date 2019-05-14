
var months = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May.', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.']
var oTbody = document.getElementById('tbody');
var oMonYear = document.getElementById('caption');
var oLow = oTbody.getElementsByClassName('low');
var newYear = new Date().getFullYear();//目前系统时间是哪一年
var nowMonth = new Date().getMonth() + 1;//目前系统时间是哪一月
var nowDay = new Date().getDate();//目前系统时间是几号
var date = new Date(newYear + "/" + nowMonth + "/1");
var index = date.getDay();//0(星期日)-6(星期六)
var days = 0;

oMonYear.innerHTML = months[nowMonth - 1] + newYear.toString();

if (nowMonth == 2 || nowMonth == 4 || nowMonth == 6 || nowMonth == 9 || nowMonth == 11) {
    days = 30;
}
else if (nowMonth == 2) {
    if (newYear % 4 == 0 || newYear % 100 == 0) {
        days = 29;
    }
    else {
        days = 28;
    }
}
else {
    days = 31;
}

var iday = 1;

for (var i = 0; i < oLow.length; i++) {
    var aTd = oLow[i].getElementsByTagName('td');
    for (var j = index; j < aTd.length; j++) {
        var html = iday.toString();
        aTd[j].innerHTML = '<span>' + html + '</span>';
        if (nowDay == html) {
            aTd[j].className = 'today';
        }
        if (iday == days) {
            if (i == 5) {
                aLow[i].css = "display", "none";
            }
            break;
        }
        iday++
    }
    aTd = [];
    index = 0;
}
