function onload1() {
    var broadcast = document.getElementById("broadcast"),
        img_list = document.getElementById("img_list"),
        button_list = document.getElementById("button_list").getElementsByTagName("li"),
        index = 0,
        timer = null,
		pre=document.getElementById('prev'),
		next=document.getElementById('next');
        //初始化
        if (timer) {
            clearInterval(timer);
            timer = null;
        }
   
        // 自动切换
        timer = setInterval(autoPlay, 3500);
   
        // 调用自动播放函数
        function autoPlay() {
            index++;
            if (index >= button_list.length) {
                index = 0;
            }
            imgChange(index);
        }
	next.onclick=function(){
		index += 1;
		if(index >= button_list.length){
			index = 0;
		}
		imgChange(index);
	}
	pre.onclick=function(){
		index -= 1;
		if(index<0){
			index = button_list.length-1;
		}
		imgChange(index);
	}

    function imgChange(buttonIndex) {
        for (let i = 0; i < button_list.length; i++) {
            button_list[i].className="";
        }
        button_list[buttonIndex].className = "first-li";//按钮样式切换
        img_list.style.marginLeft = -880 * buttonIndex + "px";
        index = buttonIndex;
    }
    //鼠标接触div
    broadcast.onmouseover = function(){
        clearInterval(timer);

    }
    //鼠标离开div
    broadcast.onmouseout = function(){
        timer = setInterval(autoPlay, 2000);
    }
    //鼠标悬停ol
    for (var i = 0; i < button_list.length; i++) {
        button_list[i].id = i;
        button_list[i].onmouseover = function() {
            clearInterval(timer);
            imgChange(this.id);
        }
    }
}
function onload2(){

	var Node=document.getElementsByClassName("dropdown-content")[0].getElementsByTagName("li");
	var ShowDiv=document.getElementsByClassName("hotnews_box")[0].getElementsByTagName("div");
	for(var i=0;i<Node.length;i++)
	{
		Node[i].index=i;
		Node[i].onclick=function()  
		{
			for(var j=0;j<Node.length;j++)
			{
				Node[j].className="";
				ShowDiv[j].className="hidden";
			}
			Node[this.index].className="select";
			ShowDiv[this.index].className="active";
		}
	}
}

window.onload=function(){
	
	onload2();
	onload1();
}