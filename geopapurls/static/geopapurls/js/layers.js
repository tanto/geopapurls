define('LayerCtrl',{
	endUrl: '/mapurls',
	dataTabledata: [],
	getlayers: function(substring){
		//if (typeof substring != 'undefined'){
		this.load();
	},
	load: function(){
		var _this = this;
		$.get(this.endUrl,$.proxy(this.success,this))
		.then(function(){
			_this.renderdata();
		})
	},
	success: function(data){
		this.convert(data);
		var a = 1;
	},
	convert: function(data){
		var _this = this;
		$(data).each(function(){ // itero sugli oggetti layer
			var layer = [];
			$.each(this,function(k,v){
				layer.push(v); // appendo il valore di ogni attributo dell'oggetto
			})
			_this.dataTabledata.push(layer);
			//console.log(this.title);
		})
	},
	renderdata: function(){
		var tableEl = $('#layersDataTable');
		tableEl.dataTable({
			"iDisplayLength": 25,
	        "bProcessing": true,
	        "bLengthChange": false,
	        "aaSorting": [[ 1, "asc" ]],
	        "aoColumns": [
		      {"bSearchable": false,"bSortable":false},
		      {"bSearchable": true},
		      {"bSearchable": true}
		    ],
	        "aaData": this.dataTabledata
		});
	}
})

$(function(){
	require(['LayerCtrl'],function(ctr){
		ctr.getlayers();
	})
})