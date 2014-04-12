define('LayerCtrl',{
	endUrl: '/mapurls',
	dataTabledata: [],
	getlayers: function(substring){
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
		this.dataTabledata = data;
	},
	renderdata: function(){
		var tableEl = $('#layersDataTable');
		tableEl.dataTable({
			"fnRowCallback": function( nRow, aData, iDisplayIndex ) {
				var layer_id = aData['id'];
				var actions = '<a href="/mapurls/'+layer_id+'/preview" target="_blank">Preview</a>&nbsp \
								<a href="/mapurls/'+layer_id+'" target="_blank">Mapurl</a>&nbsp \
								<a href="/mapurls/'+layer_id+'/download" target="_blank">Download</a>';
	            $('td:eq(2)', nRow).html(actions);
	        },
			"iDisplayLength": 25,
	        "bProcessing": true,
	        "bLengthChange": false,
	        "aaSorting": [[ 1, "asc" ]],
	        "aoColumns": [
		      {"mDataProp": "service","bSearchable": true,"sWidth": "15%" },
		      {"mDataProp": "title","bSearchable": true,"sWidth": "65%" },
		      {"mDataProp": "","bSearchable": false,"bSortable": false,"sWidth": "20%","sDefaultContent":"Preview","sClass": "center",}
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