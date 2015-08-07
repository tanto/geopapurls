var app = angular.module('app', ['filters','ngTouch', 'ui.grid', 'ui.grid.pagination','leaflet-directive']);

app.factory("SpatialFilterSrv",function(){
    var service = {
        defBounds: {
            n: 90,
            s: -90,
            e: 180,
            w: -180
        },
        bounds: {
            n: 90,
            s: -90,
            e: 180,
            w: -180
        },
        isFilterSet: function(){
            if (service.bounds.n >= 90 && service.bounds.s <= -90 && service.bounds.e >= 180 && service.bounds.w <= -180){
                return false;
            }
            return true;
        }
    }
    return service
})

app.controller('MainCtrl', ['$scope', '$http','uiGridConstants','SpatialFilterSrv', function ($scope,$http,uiGridConstants,SpatialFilterSrv) {
        
    var paginationOptions = {
        pageNumber: 1,
        pageSize: 25,
        sort: {
            sortcol: 'id',
            sortdir: 'desc',
            sortcolDef: 'id',
            sortdirDef: 'desc'
        },
        filters: {
            filtercols: [],
            filterterms: [],
        },
        bounds: null
    };
    
    var baseUrl = '/mapurlshtml'
    
    $scope.gridOptions = {
        columnDefs : [
            {name: "Service", field: "service",width: "40%",enableHiding : false},
            {name: "Title", field: "title", width: "40%",enableHiding : false},
            {name: "Tools", field: "id", cellTemplate: '<a href="/mapurls/{{row.entity[\'id\']}}/preview" target="_blank">Preview</a>&nbsp \
								<a href="/mapurls/{{row.entity[\'id\']}}" target="_blank">Mapurl</a>&nbsp \
								<a href="/mapurls/{{row.entity[\'id\']}}/download" target="_blank">Download</a>',width: '20%',enableSorting:false,enableFiltering:false,enableHiding : false,enableColumnMenu:false}],
        paginationPageSizes: [25, 50, 100],
        paginationPageSize: 25,
        useExternalPagination: true,
        enableFiltering: true,
        useExternalFiltering: true,
        useExternalSorting: true,
        enableHorizontalScrollbar: uiGridConstants.scrollbars.NEVER,
        onRegisterApi: function(gridApi) {
            $scope.gridApi = gridApi;
            $scope.gridApi.core.on.sortChanged( $scope, $scope.sortChanged );
            $scope.gridApi.core.on.filterChanged( $scope, debounce($scope.filterChanged,300) );
            gridApi.pagination.on.paginationChanged($scope, function (newPage, pageSize) {
                paginationOptions.pageNumber = newPage;
                paginationOptions.pageSize = pageSize;
                $scope.getPage();
            })
        }
    }
    
    $scope.filterChanged = function () {
        var filtercols = [];
        var filterterms = [];
        angular.forEach(this.grid.columns,function(col,k){
            if (col.filters.length > 0 && col.filters[0].term != null){
                filtercols.push(col.field);
                filterterms.push(col.filters[0].term);
            }
        })
        paginationOptions.filters['filtercols'] = filtercols;
        paginationOptions.filters['filterterms'] = filterterms;
        $scope.getPage();
    }
    
    $scope.sortChanged = function ( grid, sortColumns ) {
        if (sortColumns.length > 0) {
            var maxpriority = 0;
            angular.forEach(sortColumns,function(sortCol,k){
                priority = sortCol.sort.priority;
                if (priority > maxpriority){
                    maxpriority = priority
                }
            })
            idx = priority - 1;
            var sortdir = sortColumns[idx].sort.direction;
            var sortcol = sortColumns[idx].field;
        }
        else {
            var sortdir = paginationOptions.sort['sortdirDef'];
            var sortcol = paginationOptions.sort['sortcolDef'];
        }
        paginationOptions.sort['sortcol'] = sortcol;
        paginationOptions.sort['sortdir'] = sortdir;
        $scope.getPage();
    }
      
    $scope.getPage = function() {
        var sortcol = paginationOptions.sort['sortcol'];
        var sortdir = paginationOptions.sort['sortdir'];
        var filters = paginationOptions.filters;
        var url = baseUrl+'?sc='+sortcol+'&sd='+sortdir+'&l='+paginationOptions.pageSize+'&o='+((paginationOptions.pageNumber - 1) * paginationOptions.pageSize)+'&'+make_filter_query(filters);
        if (paginationOptions.bounds != null){
            var bounds = paginationOptions.bounds;
            url += '&b='+bounds.n+','+bounds.w+','+bounds.s+','+bounds.e;
        }
        $http.get(url)
        .success(function (data) {
          $scope.gridOptions.totalItems = data.total;
          $scope.gridOptions.data = data.data;
        });
    }

    $scope.$watchCollection(function(){return SpatialFilterSrv.bounds},function(){
            if(SpatialFilterSrv.isFilterSet()){
                paginationOptions.bounds = SpatialFilterSrv.bounds;
            }
            else{
                paginationOptions.bounds = null;
            }
            $scope.getPage();
    })
    
    var make_filter_query = function(filters){
        var querystring = '';
        var filtercols = [];
        var filterterms = [];
        angular.forEach(filters.filtercols,function(col,idx){
            if (filters.filterterms[idx] != ''){
                filtercols.push(col);
                filterterms.push(filters.filterterms[idx]);
            }
        })
        querystring += 'fc='+filtercols.join('!!!');
        querystring += '&ft='+filterterms.join('!!!');
        return querystring;
    }
    
    function debounce(func, wait, immediate) {
        var timeout;
        return function() {
            var context = this, args = arguments;
            var later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            var callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
	};
};

    //$scope.getPage();
}
]);

app.controller("SpatialFilterCtrl",['$scope','SpatialFilterSrv','leafletData',function($scope,SpatialFilterSrv,leafletData){
    $scope.bounds = SpatialFilterSrv.bounds;
    
    $scope.setFilter = function(){
        var asbounds = areaselect.getBounds();
        var bounds = {
            n: asbounds.getNorth(),
            s: asbounds.getSouth(),
            e: asbounds.getEast(),
            w: asbounds.getWest()
        }
        setBounds(bounds);
    }
    
    var setBounds = function(bounds){
        $scope.bounds.n = bounds.n;
        $scope.bounds.s = bounds.s;
        $scope.bounds.e = bounds.e;
        $scope.bounds.w = bounds.w;
    }
    
    $scope.isFilterSet = SpatialFilterSrv.isFilterSet;
    
    $scope.resetFilter = function(){
        setBounds(SpatialFilterSrv.defBounds);
    }
    
    var areaselect = L.areaSelect({width:200, height:300});
    
    leafletData.getMap().then(function(map){
        areaselect.addTo(map);
    });
    
    angular.element("#ssModal").on('shown.bs.modal', function(){
        leafletData.getMap().then(function(map){map.invalidateSize()});
     });
}
])

angular.module('filters', []).filter('npad', function($sce) {
	return function(input) {
        try{
            coord = parseFloat(input);
            if (coord>0){
                input = String.fromCharCode(160)+input;
            }
            return $sce.trustAsHtml(input);
        }
        catch (ex){
            return input;
        }
	};
});
