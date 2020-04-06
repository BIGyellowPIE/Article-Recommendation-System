function func(){

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
 window.onload=func;