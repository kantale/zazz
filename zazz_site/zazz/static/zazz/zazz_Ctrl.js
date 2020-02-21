app.controller('zazz_Ctrl', function($scope, $http, $timeout) {

	$scope.init = function() {

//        $scope.columns = {
//            sample: {
//                    field: 'sample',
//                    title: 'Sample',
//                    //filterControl:"input",
//                    sortable:true,
//                    width:'10%'
//                },
//            Bases: {
//                    field: 'Bases',
//                    title: 'Bases',
//                    sortable: true,
//                    width:'10%'
//                },
//            Barcode_Name: {
//                    field: 'Barcode_Name',
//                    title: 'Barcode_Name',
//                    sortable: true,
//                    //filterControl: "select",
//                    //filterData: "url:Barcode_Name/",
//                    width:'10%'
//                }
//
//        };
//
//        $scope.btable = {
//            url:"sample_table/",
//            //filterControl:true,
//            pagination:true,
//            sidePagination:"server",
//            filterShowClear:true,
//
//            columns: []
//        };
//
//       //ts_fff($scope.btable);


        //$scope.field_selected = [false, false, false];
        $scope.current_filter = {}; //The filter that will be applied 

        //$scope.table_data = []; // Data to be added in table

        $scope.count = '(unknown)';

        //Pagination
        $scope.currentPage = 0;
        $scope.gap = 5;
        $scope.itemsPerPage = 20;
        $scope.pagedItems = []; 

        $scope.table_data = []; // The data that we show on the table
        $scope.explore_data = []; //The data that we explore through dc

        //Explore
        $scope.e_rows = [];
        $scope.e_components = 0;

        $scope.ndx = undefined;
	};

    //https://stackoverflow.com/questions/24081004/angularjs-ng-repeat-filter-when-value-is-greater-than
    $scope.greaterThan = function(prop, val){
        return function(item){
        return item[prop] > val;
        }
    }

    $scope.e_selected = {}; // selected of the expand seledt ui. https://github.com/angular-ui/ui-select/issues/1353

    // https://github.com/angular-slider/angularjs-slider


//        $scope.fields_OLD = [
//            //{'name': 'sample', 'type': 'checkbox', 'selected': false, 'itemArray': [{id: 1, name: ''}], 'selected2': {'value': {id: 1, name: ''}} },
//            {'name': 'sample', 'type': 'checkbox', 'selected': false, 'itemArray': [], 'selected2': ['ALL'], 'e_order': -1 }, 
//            {'name': 'Bases', 'type': 'slider', 'selected': false, 'slider': {
//                                                                                'min': 30,
//                                                                                'max': 70,
//                                                                                'options': {
//                                                                                    'floor': 1,
//                                                                                    'ceil': 100,
//                                                                                    'disabled': true,
//                                                                                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
//                                                                                        console.log('Slider changed');
//                                                                                        //console.log(modelValue); // This the min
//                                                                                        //console.log(highValue); // This is the max
//                                                                                        $scope.update_table();
//                                                                                    }
//                                                                                },
//                                                                            }, 
//                'e_order': -1}, 
//            {'name':'Barcode_Name', 'type':'checkbox', 'selected': false, 'itemArray': [], 'selected2': ['ALL'], 'e_order': -1 }
//        ];

// FIELDS BEGIN
$scope.fields=[{'name': 'Chromosome', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 1 },
{'name': 'Position', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 20, 'order': 2 },
{'name': 'Reference', 'type': 'freetext', 'selected': false, 'e_order': -1, 'database': 'normal', 'text' : '', 'order': 3 },
{'name': 'Alternative', 'type': 'freetext', 'selected': false, 'e_order': -1, 'database': 'normal', 'text' : '', 'order': 4 },
{'name': 'RAW_NS', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 11 },
{'name': 'RAW_HS', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 12 },
{'name': 'RAW_DP', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 13 },
{'name': 'RAW_RO', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 14 },
{'name': 'RAW_AO', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 15 },
{'name': 'RAW_SRF', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 16 },
{'name': 'RAW_SRR', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 17 },
{'name': 'RAW_SAF', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 18 },
{'name': 'RAW_SAR', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 19 },
{'name': 'RAW_FDP', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 20 },
{'name': 'RAW_FRO', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 21 },
{'name': 'RAW_FAO', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 22 },
{'name': 'RAW_AF', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 23 },
{'name': 'RAW_QD', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 24 },
{'name': 'RAW_FSRF', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 25 },
{'name': 'RAW_FSRR', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 26 },
{'name': 'RAW_FSAF', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 27 },
{'name': 'RAW_FSAR', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 28 },
{'name': 'RAW_FXX', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 29 },
{'name': 'RAW_TYPE', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 30 },
{'name': 'RAW_LEN', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 31 },
{'name': 'RAW_HRUN', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 32 },
{'name': 'RAW_FR', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 33 },
{'name': 'RAW_RBI', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 34 },
{'name': 'RAW_FWDB', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 35 },
{'name': 'RAW_REVB', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 36 },
{'name': 'RAW_REFB', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 37 },
{'name': 'RAW_VARB', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 38 },
{'name': 'RAW_SSSB', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 39 },
{'name': 'RAW_SSEN', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 40 },
{'name': 'RAW_SSEP', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 41 },
{'name': 'RAW_STB', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 42 },
{'name': 'RAW_STBP', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 43 },
{'name': 'RAW_PB', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 44 },
{'name': 'RAW_PBP', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 45 },
{'name': 'RAW_MLLD', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 46 },
{'name': 'RAW_OID', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 47 },
{'name': 'RAW_OPOS', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 48 },
{'name': 'RAW_OREF', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 49 },
{'name': 'RAW_OALT', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 50 },
{'name': 'RAW_OMAPALT', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 51 },
{'name': 'RAW_GT_GT', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 52 },
{'name': 'RAW_GT_GQ', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 53 },
{'name': 'RAW_GT_DP', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 54 },
{'name': 'RAW_GT_RO', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 55 },
{'name': 'RAW_GT_AO', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 56 },
{'name': 'RAW_GT_SRF', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 57 },
{'name': 'RAW_GT_SRR', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 58 },
{'name': 'RAW_GT_SAF', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 59 },
{'name': 'RAW_GT_SAR', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 60 },
{'name': 'RAW_GT_FDP', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 61 },
{'name': 'RAW_GT_FRO', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 62 },
{'name': 'RAW_GT_FAO', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 63 },
{'name': 'RAW_GT_AF', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 64 },
{'name': 'RAW_GT_FSRF', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 65 },
{'name': 'RAW_GT_FSRR', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 66 },
{'name': 'RAW_GT_FSAF', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 67 },
{'name': 'RAW_GT_FSAR', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 68 },
{'name': 'ION_Type', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 102 },
{'name': 'ION_Reference', 'type': 'freetext', 'selected': false, 'e_order': -1, 'database': 'normal', 'text' : '', 'order': 105 },
{'name': 'ION_Length', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 20, 'order': 106 },
{'name': 'ION_Genotype', 'type': 'freetext', 'selected': false, 'e_order': -1, 'database': 'normal', 'text' : '', 'order': 107 },
{'name': 'ION_PValue', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 20, 'order': 108 },
{'name': 'ION_Coverage', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 20, 'order': 109 },
{'name': 'ION_Allele_Coverage_1', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 20, 'order': 110 },
{'name': 'ION_Allele_Coverage_2', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 20, 'order': 111 },
{'name': 'ION_MAF', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 112 },
{'name': 'ION_Gene', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ION_Transcripts', 'order': 113 },
{'name': 'ION_Transcript', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ION_Transcripts', 'order': 114 },
{'name': 'ION_Location', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ION_Transcripts', 'order': 115 },
{'name': 'ION_Function', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ION_Transcripts', 'order': 116 },
{'name': 'ION_Codon', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ION_Transcripts', 'order': 117 },
{'name': 'ION_Exon', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ION_Transcripts', 'order': 118 },
{'name': 'ION_Protein', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ION_Transcripts', 'order': 119 },
{'name': 'ION_Coding', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ION_Transcripts', 'order': 120 },
{'name': 'ION_Sift', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'table': 'ION_Transcripts', 'order': 121 },
{'name': 'ION_Polyphen', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'table': 'ION_Transcripts', 'order': 122 },
{'name': 'ION_Grantham', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'table': 'ION_Transcripts', 'order': 123 },
{'name': 'ION_NormalizedAlt', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ION_Transcripts', 'order': 124 },
{'name': 'ION_F5000Exomes_AMAF', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 125 },
{'name': 'ION_F5000Exomes_EMAF', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 126 },
{'name': 'ION_F5000Exomes_GMAF', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 127 },
{'name': 'ION_Clinvar', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 128 },
{'name': 'ION_COSMIC', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'renderer': 
                        function(x) {
                            if (x.ION_COSMIC != 'NaN') {
                                return "<a href=https://cancer.sanger.ac.uk/cosmic/search?q=" + x.ION_COSMIC + ">" + x.ION_COSMIC + "</a>";
                            }
                            return 'NaN';
                        }
                        , 'table': 'ION_cosmic', 'order': 129 },
{'name': 'ION_DbSNP', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'renderer': 
                        function(x) {
                            if (x.ION_DbSNP != 'NaN') {
                                return "<a href=https://www.ncbi.nlm.nih.gov/snp/" + x.ION_DbSNP + ">" + x.ION_DbSNP + "</a>";
                            }
                            return 'NaN';
                        }

                        , 'table': 'ION_dbsnp', 'order': 130 },
{'name': 'ION_Drugbank', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ION_drugbank', 'order': 131 },
{'name': 'ION_GO', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ION_go', 'order': 132 },
{'name': 'ION_OMIM', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'renderer': 
                function(x) {
                    if (x.ION_OMIM != 'NaN') {
                        return "<a href=https://www.omim.org/entry/" + x.ION_OMIM + ">" + x.ION_OMIM + "</a>";
                    }
                    return 'NaN';
                }
            , 'table': 'ION_omim', 'order': 133 },
{'name': 'ION_Pfam', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'renderer': 
                function(x) {
                    if (x.ION_Pfam != 'NaN') {
                        return "<a href=https://pfam.xfam.org/family/" + x.ION_Pfam + ">" + x.ION_Pfam + "</a>";
                    }
                    return 'NaN';
                }
            , 'table': 'ION_pfam', 'order': 134 },
{'name': 'ION_Phylop', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'table': 'ION_phylop', 'order': 135 },
{'name': 'ANN_Func_refGene', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 201 },
{'name': 'ANN_Gene_refGene', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 202 },
{'name': 'ANN_GENEDETAIL_REFGENE', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ANN_GeneDetail_refGene', 'order': 203 },
{'name': 'ANN_ExonicFunc_refGene', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 204 },
{'name': 'ANN_AAChange_refGene_gene', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ANN_AAChange_refGene', 'order': 205 },
{'name': 'ANN_AAChange_refGene_transcript', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ANN_AAChange_refGene', 'order': 206 },
{'name': 'ANN_AAChange_refGene_exon', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ANN_AAChange_refGene', 'order': 207 },
{'name': 'ANN_AAChange_refGene_coding', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ANN_AAChange_refGene', 'order': 208 },
{'name': 'ANN_AAChange_refGene_protein', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ANN_AAChange_refGene', 'order': 209 },
{'name': 'ANN_cytoBand', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 210 },
{'name': 'ANN_ExAC_ALL', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 211 },
{'name': 'ANN_ExAC_AFR', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 212 },
{'name': 'ANN_ExAC_AMR', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 213 },
{'name': 'ANN_ExAC_EAS', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 214 },
{'name': 'ANN_ExAC_FIN', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 215 },
{'name': 'ANN_ExAC_NFE', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 216 },
{'name': 'ANN_ExAC_OTH', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 217 },
{'name': 'ANN_ExAC_SAS', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 218 },
{'name': 'ANN_avsnp147', 'type': 'freetext', 'selected': false, 'e_order': -1, 'database': 'normal', 'text' : '', 'order': 219 },
{'name': 'ANN_SIFT_score', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 220 },
{'name': 'ANN_SIFT_pred', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 221 },
{'name': 'ANN_Polyphen2_HDIV_score', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 222 },
{'name': 'ANN_Polyphen2_HDIV_pred', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 223 },
{'name': 'ANN_Polyphen2_HVAR_score', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 224 },
{'name': 'ANN_Polyphen2_HVAR_pred', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 225 },
{'name': 'ANN_LRT_score', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 226 },
{'name': 'ANN_LRT_pred', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 228 },
{'name': 'ANN_MutationTaster_score', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 229 },
{'name': 'ANN_MutationTaster_pred', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 230 },
{'name': 'ANN_MutationAssessor_score', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 231 },
{'name': 'ANN_MutationAssessor_pred', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 232 },
{'name': 'ANN_FATHMM_score', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 233 },
{'name': 'ANN_FATHMM_pred', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 234 },
{'name': 'ANN_PROVEAN_score', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 235 },
{'name': 'ANN_PROVEAN_pred', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 236 },
{'name': 'ANN_VEST3_score', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 237 },
{'name': 'ANN_CADD_raw', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 238 },
{'name': 'ANN_CADD_phred', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 239 },
{'name': 'ANN_DANN_score', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 240 },
{'name': 'ANN_fathmm_MKL_coding_score', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 241 },
{'name': 'ANN_fathmm_MKL_coding_pred', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 242 },
{'name': 'ANN_MetaSVM_score', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 243 },
{'name': 'ANN_MetaSVM_pred', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 244 },
{'name': 'ANN_MetaLR_score', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 245 },
{'name': 'ANN_MetaLR_pred', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 246 },
{'name': 'ANN_integrated_fitCons_score', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 247 },
{'name': 'ANN_integrated_confidence_value', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'xUnits': 10, 'order': 248 },
{'name': 'ANN_GERP', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 249 },
{'name': 'ANN_phyloP7way_vertebrate', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 250 },
{'name': 'ANN_phyloP20way_mammalian', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 251 },
{'name': 'ANN_phastCons7way_vertebrate', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 252 },
{'name': 'ANN_phastCons20way_mammalian', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 253 },
{'name': 'ANN_SiPhy_29way_logOdds', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'order': 254 },
{'name': 'ANN_CLNALLELEID', 'type': 'freetext', 'selected': false, 'e_order': -1, 'database': 'normal', 'text' : '', 'order': 255 },
{'name': 'ANN_CLNDN', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ANN_CLINVAR', 'order': 256 },
{'name': 'ANN_CLNDISDB', 'type': 'freetext', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'text' : '', 'table': 'ANN_CLINVAR', 'order': 257 },
{'name': 'ANN_CLNREVSTAT', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 258 },
{'name': 'ANN_CLNSIG', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 259 },
{'name': 'VEP_Allele', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 301 },
{'name': 'VEP_Consequence', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 302 },
{'name': 'VEP_IMPACT', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 302 },
{'name': 'VEP_SYMBOL', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 303 },
{'name': 'VEP_Gene', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 303 },
{'name': 'VEP_Feature_type', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 304 },
{'name': 'VEP_Feature', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 305 },
{'name': 'VEP_BIOTYPE', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 306 },
{'name': 'VEP_EXON', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 307 },
{'name': 'VEP_INTRON', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 308 },
{'name': 'VEP_HGVSc', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 309 },
{'name': 'VEP_HGVSp', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 310 },
{'name': 'VEP_cDNA_position', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 311 },
{'name': 'VEP_CDS_position', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 312 },
{'name': 'VEP_Amino_acids', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 313 },
{'name': 'VEP_Codons', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 314 },
{'name': 'VEP_Existing_variation', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 315 },
{'name': 'VEP_DISTANCE', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 316 },
{'name': 'VEP_STRAND', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 317 },
{'name': 'VEP_FLAGS', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 318 },
{'name': 'VEP_VARIANT_CLASS', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 319 },
{'name': 'VEP_SYMBOL_SOURCE', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 320 },
{'name': 'VEP_HGNC_ID', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 321 },
{'name': 'VEP_CANONICAL', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 322 },
{'name': 'VEP_TSL', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 323 },
{'name': 'VEP_APPRIS', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 324 },
{'name': 'VEP_CCDS', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 325 },
{'name': 'VEP_ENSP', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 326 },
{'name': 'VEP_SWISSPROT', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 327 },
{'name': 'VEP_TREMBL', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 328 },
{'name': 'VEP_UNIPARC', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 329 },
{'name': 'VEP_GENE_PHENO', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 330 },
{'name': 'VEP_SIFT', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 331 },
{'name': 'VEP_PolyPhen', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 332 },
{'name': 'VEP_miRNA', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 334 },
{'name': 'VEP_HGVS_OFFSET', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 335 },
{'name': 'VEP_AF', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 336 },
{'name': 'VEP_AFR_AF', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 337 },
{'name': 'VEP_AMR_AF', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 338 },
{'name': 'VEP_EAS_AF', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 339 },
{'name': 'VEP_EUR_AF', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 340 },
{'name': 'VEP_SAS_AF', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 341 },
{'name': 'VEP_AA_AF', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 342 },
{'name': 'VEP_EA_AF', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 343 },
{'name': 'VEP_gnomAD_AF', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 344 },
{'name': 'VEP_gnomAD_AFR_AF', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 345 },
{'name': 'VEP_gnomAD_AMR_AF', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 346 },
{'name': 'VEP_gnomAD_ASJ_AF', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 347 },
{'name': 'VEP_gnomAD_EAS_AF', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 348 },
{'name': 'VEP_gnomAD_FIN_AF', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 349 },
{'name': 'VEP_gnomAD_NFE_AF', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 350 },
{'name': 'VEP_gnomAD_OTH_AF', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 351 },
{'name': 'VEP_gnomAD_SAS_AF', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 352 },
{'name': 'VEP_MAX_AF', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 353 },
{'name': 'VEP_MAX_AF_POPS', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 354 },
{'name': 'VEP_CLIN_SIG', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 355 },
{'name': 'VEP_SOMATIC', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 356 },
{'name': 'VEP_PHENO', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 357 },
{'name': 'VEP_PUBMED', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 358 },
{'name': 'VEP_MOTIF_NAME', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 359 },
{'name': 'VEP_MOTIF_POS', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 360 },
{'name': 'VEP_HIGH_INF_POS', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'VEP_MULTI', 'order': 361 },
{'name': 'VEP_MOTIF_SCORE_CHANGE', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'slider': {
                'min': 30,
                'max': 70,
                'options': {
                    'floor': 1,
                    'ceil': 100,
                    'disabled': true,
                    'onEnd' : function (sliderId, modelValue, highValue, pointerType) {
                        console.log('Slider changed');
                        //console.log(modelValue); // This the min
                        //console.log(highValue); // This is the max
                        $scope.update_table();
                    }
                },
            }, 'table': 'VEP_MULTI', 'order': 362 },
{'name': 'CLINVARZAZZ_interpretation', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ZAZZ_CLINVAR', 'order': 401 },
{'name': 'CLINVARZAZZ_scv_review_status', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ZAZZ_CLINVAR', 'order': 402 },
{'name': 'CLINVARZAZZ_clinical_significance', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ZAZZ_CLINVAR', 'order': 403 },
{'name': 'CLINVARZAZZ_condition_name', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ZAZZ_CLINVAR', 'order': 404 },
{'name': 'CLINVARZAZZ_rcv_review_status', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ZAZZ_CLINVAR', 'order': 405 },
{'name': 'CLINVARZAZZ_review_status_stars', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi_1', 'itemArray': [], 'selected2': ['ALL'], 'table': 'ZAZZ_CLINVAR', 'order': 406 }];
// FIELDS END


//    $scope.itemArray = [
//        {id: 1, name: ''},
//    ];
//
//    $scope.selected = { value: $scope.itemArray[0] };



        /*
        * Helper function that perform ajax calls
        * success_view: what to do if data were correct and call was successful
        * fail_view: What to do if call was succesful but data where incorrect
        * fail_ajax: what to do if ajax call was incorrect
        */
        $scope.ajax = function(url, data, success_view, fail_view, fail_ajax) {
                // URL should always end with '/'

                console.log('Before Ajax, data:');
                console.log(data);

                data.csrftoken = CSRF_TOKEN;

                $http({
                        headers: {
                                "Content-Type": 'application/json',
                                "Access-Control-Allow-Origin": "*", // TODO : REMOVE THIS!
                                //"X-CSRFToken" : getCookie('csrftoken'),
                                "X-CSRFToken" : window.CSRF_TOKEN,
                        },
                    method : "POST",
                    url : url,
                    data : data
                }).then(function mySucces(response) {
                    // $scope.myWelcome = response.data;
                    // alert(JSON.stringify(response));
                    if (response['data']['success']) {
                        console.log('AJAX SUCCESS:');
                        console.log(response['data']['success']);
                        success_view(response['data']);
                    }
                    else {
                        console.log('AJAX ERROR:');
                        fail_view(response['data']);
                    }
                    
                }, function myError(response) {
                        fail_ajax(response.statusText);
                });
        };

    $scope.get_database_checkbox = function(component) {
        $scope.ajax(
            'get_database_checkbox/',
            {
                field:component.name,
                database:component.database, //normal, none_not_none
                filter:$scope.current_filter,
                table: component.hasOwnProperty('table') ? component.table : '__TSATSARA__'
            },
            function(response) {
                //console.log(response);
                //$scope.itemArray = response.results;
                component.itemArray = response.results;
            },
            function(response) {

            },
            function(statusText) {
                alert(statusText);
            }
        );
    };

    $scope.midpoint = function(a,b) {
        return a + (b-a)/2;
    };

    $scope.get_database_slider = function(component) {

        console.log('COMPONENT:')
        console.log(component);
        var table = null;

        if ('database' in component) {
            if (component.database == 'multi_1') {
                table = component.table;
            }
        }

        $scope.ajax(
            'get_database_slider/',
            {
                field:component.name,
                filter:$scope.current_filter,
                table:table
            },
            function(response) {
                var av = $scope.midpoint(response.results.min, response.results.max);
                component.slider.options.floor = response.results.min;
                component.slider.options.ceil = response.results.max;

                // If The difference between min and max is small (<5), the change the resolution of the slider
                if (response.results.max - response.results.min < 5) { 
                    component.slider.options.step = 0.01;
                    component.slider.options.precision = 2;
                }

                //component.slider.min = $scope.midpoint(response.results.min, av);
                component.slider.min = response.results.min;
                //component.slider.max = $scope.midpoint(av, response.results.max);
                component.slider.max = response.results.max;
                component.slider.options.disabled = false;
                console.log('slider component:');
                console.log(component.slider);

            },
            function(response) {

            },
            function(statusText) {
                alert(statusText);
            }
        );
    };

    //Builds a component
    $scope.build_component = function(component) {

        if (component.type == 'checkbox') {
            //var this_id = component.name + '_' + 'checkbox';

            $scope.get_database_checkbox(component);

        }
        else if (component.type == 'slider') {
            $scope.get_database_slider(component);
        }
    };

    //When a checkbox is changed
    $scope.selected_changed = function(x) {
        // alert(x);
        console.log('Selected_changed:');
        console.log(x);
        //console.log($scope.field_selected);

        //Empty columns
        //$scope.btable.columns = [];

        //Add only the true values;
        for (var i in $scope.fields) {
            //if ($scope.fields[i].selected) {
            //    $scope.btable.columns.push($scope.columns[$scope.fields[i].name]);
            //}

            if ((x==i) && ($scope.fields[i].selected)) {
                //This was changed AND is selected.
                //Build the component
                $scope.build_component($scope.fields[i]);
            }
        }

        //Wait for the components to be build. FIX ME!!!
        $timeout(function(){$scope.update_table();}, 500);
        

        //$('#table').bootstrapTable('refreshOptions', $scope.btable);
        // $('#table').bootstrapTable('load', {ƒtotal":2,"rows":[{"sample":"1"},{"sample":"2"}]}); // THIS WORKS
        //$('#table').bootstrapTable('refresh');  


    };

    //Creates the 'filter' option that we will pass through ajax in update_table
    $scope.build_filter = function() {
        // Samples.objects.filter(sample__in = ['MA0052'])
        // Samples.objects.filter(Bases__gte = 100)
        var ret = {};

        for (var i=0; i<$scope.fields.length; i++) {

            if (!$scope.fields[i].selected) {
                continue;
            }

            if ($scope.fields[i].hasOwnProperty('include')) {
                for (var j=0; j<$scope.fields[i].include.length; j++) {
                    ret[$scope.fields[i].include[j] + '__in'] = ['ALL'];
                }
            }

            if ($scope.fields[i].type == 'checkbox') {
                //$.inArray('ALL', $scope.fields[i].selected2) {
                //    ret[$scope.fields[i].name] = []
                //}

                if ($scope.fields[i].database == 'none_not_none') {
                    if ($scope.fields[i].selected2.length==0) {
                        ret[$scope.fields[i].name + '__in'] = [];
                    }
                    else if ($scope.fields[i].selected2.includes('ALL')) {
                        ret[$scope.fields[i].name + '__in'] = ['ALL'];
                    }
                    else if ($scope.fields[i].selected2.includes('Exists') && $scope.fields[i].selected2.includes('Missing')) {
                        ret[$scope.fields[i].name + '__in'] = ['ALL'];
                    }
                    else if ($scope.fields[i].selected2.includes('Exists')) {
                        ret[$scope.fields[i].name + '__isnull'] = false;
                    }
                    else if ($scope.fields[i].selected2.includes('Missing')) {
                        ret[$scope.fields[i].name + '__isnull'] = true;
                    }
                }
                else if ($scope.fields[i].database == 'multi_1') {

                    //Pass the database
                    ret[$scope.fields[i].name + '__table'] = $scope.fields[i].table;

                    if ($scope.fields[i].selected2.length==0) {
                        ret[$scope.fields[i].name + '__multi'] = ['__TSATSARA__']; // FIXME
                    }
                    else if ($scope.fields[i].selected2.includes('ALL')) {
                        ret[$scope.fields[i].name + '__multi'] = ['ALL'];
                    }
                    else {
                        ret[$scope.fields[i].name + '__multi'] = $scope.fields[i].selected2;
                    }

                }
                else {
                    ret[$scope.fields[i].name + '__in'] = $scope.fields[i].selected2;
                }
            }
            else if ($scope.fields[i].type == 'slider') {
                if ($scope.fields[i].database == 'multi_1') {
                    ret[$scope.fields[i].name + '__table'] = $scope.fields[i].table;
                    ret[$scope.fields[i].name + '__multi'] = {min: $scope.fields[i].slider.min, max: $scope.fields[i].slider.max};

                }
                else {
                    ret[$scope.fields[i].name + '__gte'] = $scope.fields[i].slider.min;
                    ret[$scope.fields[i].name + '__lte'] = $scope.fields[i].slider.max;
                }
            }
            else if ($scope.fields[i].type == 'freetext') {

                if ($scope.fields[i].database == 'multi_1') {
                    //Pass the database
                    ret[$scope.fields[i].name + '__table'] = $scope.fields[i].table;
                    ret[$scope.fields[i].name + '__multi'] = $scope.fields[i].text;
                }
                else {
                    ret[$scope.fields[i].name + '__icontains'] = $scope.fields[i].text;
                }
            }
        }

        return ret;
    };

    $scope.build_order = function() {

        var ret = {};

        for (var i=0; i<$scope.fields.length; i++) {
            if (!$scope.fields[i].selected) {
                continue;
            }

            if (!$scope.fields[i].hasOwnProperty('order')) {
                continue;
            }

            ret[$scope.fields[i].name] = $scope.fields[i].order;
        }

        return ret;
    };

    // When a select is changed
    // Defined in <ui-select multiple ng-model="x.selected2" ng-hide="!x.selected" theme="bootstrap" close-on-select="false" ng-change="select_changed()">
    $scope.select_changed = function() {
        console.log('select changed');
        $scope.update_table();
    };

    //When a freetext is changed
    $scope.freetext_change = function(x) {
        // x.text is the new text
        $scope.update_table();
    };

    // One of checkboxes have changed. Fetch rows from database
    $scope.update_table = function() {
        console.log('Ajax update table..');
        $scope.ajax(
            'update_table/',
            {
                'filter': $scope.build_filter(),
                'order': $scope.build_order(),
                'max_filter': 1000
            },
            function(response) {
                //$scope.table_data = response['results'];
                $scope.table_data = response['results'];
                $scope.groupToPages($scope.table_data);
                $scope.count = response['count'];

                $scope.currentPage = 0; //Show first page of the table
            },
            function(response) {

            },
            function(statusText) {
                alert(statusText);
            }
        );
    };

    $scope.sort_by = function(x) {

        alert('sort');
    };

    //Pagination
    // http://jsfiddle.net/SAWsA/1754/

    // calculate page in place
    $scope.groupToPages = function (data) {
        $scope.pagedItems = [];
        
        for (var i = 0; i < data.length; i++) {
            if (i % $scope.itemsPerPage === 0) {
                $scope.pagedItems[Math.floor(i / $scope.itemsPerPage)] = [ data[i] ];
            } else {
                $scope.pagedItems[Math.floor(i / $scope.itemsPerPage)].push(data[i]);
            }
        }
    };


    $scope.range = function (size,start, end) {
        var ret = [];        
        //console.log(size,start, end);
                      
        if (size < end) {
            end = size;
            start = size-$scope.gap;
        }

        if (start<0) {
            start = 0;
        }

        for (var i = start; i < end; i++) {
            ret.push(i);
        }        
        //console.log(ret);        
        return ret;
    };
    
    $scope.prevPage = function () {
        if ($scope.currentPage > 0) {
            $scope.currentPage--;
        }
    };
    
    $scope.nextPage = function () {
        if ($scope.currentPage < $scope.pagedItems.length - 1) {
            $scope.currentPage++;
        }
    };
    
    $scope.setPage = function () {
        $scope.currentPage = this.n;
    };

    //End of pagenation

    //Explore

    $scope.log = function(x) {
        var i = x;
        console.log(i); // https://teamtreehouse.com/community/dont-know-how-to-send-data-to-consolelog 
    };

    //The button "explore" is pressed
    $scope.explore_pressed = function() {
        //Fetch ALL data from database

        $scope.ajax(
            'update_table/',
            {
                'filter': $scope.build_filter(), //Duplicate code.. FIXME
                'order': $scope.build_order(),
                'max_filter': 0
            },
            function(response) {
                //$scope.table_data = response['results'];
                $scope.explore_data = response['results'];

                //Remove all fields
                for (var i=0; i<$scope.fields.length; i++) {
                    $scope.fields[i].e_order = -1;
                }

                $scope.e_rows = [['e_next_select']]; //Initialize exlore select
            },
            function(response) {

            },
            function(statusText) {
                alert(statusText);
            }
        );

    };

    $scope.explore_selected = function() {
        //alert('explore');

        //Create e_rows

        $scope.e_rows = [];
        var next_order = 0;
        var max_cols = 3;
        var cur_cols = 0;
        var cur_col = [];

        //console.log('e_row ΙΝΙΤ:');
        //$scope.log($scope.e_rows);

        while (true) {
            var found = false;
            console.log('looking for: ' + next_order)
            for (var i=0; i<$scope.fields.length; i++) {
                if ($scope.fields[i].e_order==next_order) {
                    found = true;
                    if (cur_cols < max_cols) {
                        //console.log('aa ' +  1);
                        cur_cols+=1;
                        cur_col.push($scope.fields[i]);
                    }
                    else {
                        //console.log('bb ' + 2);
                        cur_cols = 1;
                        $scope.e_rows.push(cur_col);
                        cur_col = [$scope.fields[i]];
                    }
                    break;
                }
            }

            if (found) {
                console.log('Found ' + next_order);
                next_order++;
            }
            else {
                console.log ('Did not find ' + next_order);
                if (cur_col.length) {
                    $scope.e_rows.push(cur_col);
                }
                break;
            }

        }

        //Add e_next_select.
        //If we haven't added all. then add a select to choose the next field
        if ((next_order < $scope.fields.length) || true) { // This does not work.. 

            if ($scope.e_rows.length == 0) {
                $scope.e_rows = [['e_next_select']];
            }
            else if ($scope.e_rows[$scope.e_rows.length-1].length<max_cols) {
                $scope.e_rows[$scope.e_rows.length-1].push('e_next_select');
            }
            else {
                $scope.e_rows.push(['e_next_select']);
            }

            //console.log('e_rows AFTER e_next_select:');
            //$scope.log($scope.e_rows);
        }

        console.log('e_rows:');
        console.log($scope.e_rows);
        

    };

    

    $scope.render_crossfilter = function() {

            //Not sure if this is required
            if (!($scope.ndx === undefined)) { 
                console.log('ndx size: ', $scope.ndx.size());
                if($scope.ndx.size() > 0) {
                     // Need to apply filter to all first
                     dc.filterAll(); 
                     // Then call remove
                     $scope.ndx.remove();
                 }
            }

            $scope.ndx = crossfilter($scope.explore_data);
            //var allDim = ndx.dimension(function(d) {return d;});
            var allDim = $scope.ndx.dimension(function(d) {return d;});
            //var ndx = crossfilter(sample_data);
            $scope.e_components = 0; // Number of explore charts shown

            //This is to avoid the following warning:
            //You are using d3.schemeCategory20c, which has been removed in D3v5. See the explanation at https://github.com/d3/d3/blob/master/CHANGES.md#changes-in-d3-50. DC is using it for backward compatibility, however it will be changed in DCv3.1. You can change it by calling dc.config.defaultColors(newScheme). See https://github.com/d3/d3-scale-chromatic for some alternatives.
            //https://github.com/dc-js/dc.js/issues/1403 
            dc.config.defaultColors(d3.schemeSet1);

            //Create column functions for the explore table
            //var column_functions = [];

            //var all = ndx.groupAll();
            var all = $scope.ndx.groupAll();

            //Build Global Position Dimension
            rafDim = $scope.ndx.dimension(function(d) {
                return d['Position'];
            }); 


            for (var i=0; i<$scope.fields.length; i++) {

                if ($scope.fields[i].e_order < 0) {
                    continue;
                }
                $scope.e_components += 1;

                var name = $scope.fields[i].name;
                console.log('Building component:', name, '  i_order: ', i);
                var theChart = undefined;

                //column_functions.push(function (d) { return d[name]; });

                if (($scope.fields[i].type == 'slider') && (name != 'Position')) {

                    console.log('Explore: ->' + name + '<-');

                    var xUnits = $scope.fields[i].xUnits;

                    console.log(1);
                    
                    //var rafChart = dc.barChart('#bbbb');
                    console.log(2);
                    //var rafDim = $scope.ndx.dimension(function(d) {
                    //    return d[name];
                    //      //   //return d['Chromosome'] + ':' + d['Position'];
                    //}); // X



                    //var rafDim = $scope.ndx.dimension(function(d) {
                        //console.log(d[name]);
                        //return d[name];}); // X
                        //return Math.round(d[name] * 100000) / 100000;
                        //return Math.round(d[name] * 100) / 100;
                    //});
                    console.log(3);

                    var numericDim = $scope.ndx.dimension(function(d) {
                        return d[name];
                    });

                    //var countPerRAF = rafDim.group().reduceCount(); // Y
                    var minimum = d3.min($scope.explore_data, function (d) { return d[name]; });
                    var maximum = d3.max($scope.explore_data, function (d) { return d[name]; });

                    if (Math.abs(minimum) > 5) { 
                        minimum = minimum-1;
                    }
                    if (Math.abs(maximum) > 5) {
                        maximum = maximum+1;
                    }


                    console.log('Minimum: ' + minimum);
                    console.log('Maximum: ' + maximum);

                    //Estimate bin size
                    //https://en.wikipedia.org/wiki/Histogram#Number_of_bins_and_width

                    //Rice Rule
                    //var l = $scope.table_data.length;
                    //console.log('l: ',l);
                    //var k = 2.0*Math.pow(l, 1/3.0);
                    //console.log('k: ', k);
                    //var bin = Math.floor(Math.log10((maximum-minimum)/k))-1;
                    //console.log('bin2:', bin2)
                    //bin = Math.pow(10, bin);
                    //console.log('bin2:');
                    //console.log(bin2);


                    //var bin = 100000000; //100 bil
                    //console.log('bin:');
                    //console.log(bin);
                    
                    //var rafGroup = rafDim.group(function(d) { return bin * Math.floor(d/bin); });

                    //bin = 0.01; // bin_width
                    //var rafGroup = rafDim.group(function(d) { return bin * Math.floor(d/bin); });
                    var numericGroup = numericDim.group().reduceCount();
                    //var rafGroup = rafDim.group(function(d) {
                    //    return d;
                    //}).reduceCount();
                    //var rafGroup = rafDim.group();


                    // https://stackoverflow.com/questions/36494956/elasticxtrue-doesnt-work-dc-js
                    function remove_empty_bins(source_group) {
                        return {
                            all:function () {
                                return source_group.all().filter(function(d) {
                                    return d.value != 0;
                                });
                            }
                        };
                    }

                    //var filtered_group = remove_empty_bins(rafGroup);
                    //console.log('POSITION DIMENSION:');
                    //console.log(rafDim);


                    //console.log('raf group:');
                    //console.log(rafGroup);

                    //var logScale = d3.scaleLog()
                    //    .domain([0.00001, 0.5])
                    //    //.range([0,])
                    //    ;


                    if (true) {
                        theChart = dc.barChart('#chart-' + name + '-count');
                        theChart
                          .width(300)
                          //.width(600)
                          .height(180)
                          .dimension(numericDim)
                          //.group(countPerRAF)
                          //.group(rafGroup)
                          .group(numericGroup)
                          //.colors(d3.scaleOrdinal().domain(["positive","negative"]).range(["#00FF00","#FF0000"]))
                          //.colorAccessor(function(d) { 
                          //                  //console.log(d);
                          //                  if(d.key >50000000) 
                          //                      return "positive"
                          //                  return "negative";})

                          .x(d3.scaleLinear().domain([minimum, maximum]))
                          //.x(d3.scaleBand())
                          //.x(d3.scaleLinear().domain([0.0, 0.5]))
                          //.x(d3.scaleLinear().domain([1, 10000000]))
                          //.x(d3.scaleLinear().domain([-0.01, 0.5]))
                          //.x(d3.scaleLog().domain([-0.01, 0.5]))
                          //.x(d3.scale.linear().domain([0, 6]))
                          //.x(logScale)
                          //.elasticY(true)
                          //.elasticX(true)
                          .elasticY(true)
                          .centerBar(true)
                          //.barPadding(1) // . Valid values are between 0-1
                          .xAxisLabel(name)
                          .yAxisLabel('Count')
                          .xUnits(function (d) { return xUnits;}) //5
                          //.xUnits(dc.units.fp.precision(bin))
                          //.xUnits(dc.units.fp.precision(0.01))
                          //.xUnits(dc.units.ordinal)
                          //.mouseZoomable(true)
                          .margins({top: 10, right: 20, bottom: 50, left: 50});

                        //theChart.yAxis().ticks(0.0); // REMOVE Y AXIS
                        //theChart.xAxis().tickFormat(function(v) {return v + 'K';});
                    }

                    //theChart.on('pretransition', function(chart){
                    //    //chart.focus([1,10000000]);
                    //    chart.filter([1,100000000]);
                    //
                    //});

//                    theChart.xAxis()
//                      .tickFormat(function (v) {return v/bin ;});
                      //.ticks(2);

                    console.log(4);
                    //dc.renderAll();
                    //$timeout(function(){dc.renderAll();}, 2000);
                }

                else if ($scope.fields[i].type == 'checkbox') {
                    console.log('Explore: ->' + name + '<-');
                    
                    //var selectDim = ndx.dimension(function(d) { return d[name]; });

                    var selectDim;
                    if ($scope.fields[i].database == 'none_not_none') {
                        selectDim = $scope.ndx.dimension(function(d) {
                            if (d[name] == null) {
                                return 'Missing';
                            }
                            return 'Exists';
                        });
                    }
                    else {
                        selectDim = $scope.ndx.dimension(function(d) { return d[name]; });
                    }

                    if (true) {

                        theChart = dc.selectMenu('#chart-' + name + '-count');
                        theChart
                            .dimension(selectDim)
                            .group(selectDim.group())
                            .multiple(true)
                            .numberVisible(15)
                            .controlsUseVisibility(true);
                    }
                    if (false) {
                        theChart = dc.pieChart('#chart-' + name + '-count');
                        theChart
                            .dimension(selectDim)
                            .group(selectDim.group())
                            .radius(90)
                            .innerRadius(40)
                            .colors(d3.scaleOrdinal(d3.schemeCategory20b))
                            .label(function(d) {
                                console.log(d);
                                var perc = Math.floor(d.value / all.value() * 100) + '%';
                                //return d.key + ' (' + perc + ')' ;
                                return d.key + ' (' + d.value + ')';

                            })
                            ;
                    }
                    if (false) {

                        var all_possible_values = [];
                        var this_group = $scope.ndx.dimension(function (d) { return d[name]});
                    
                        this_group.group().all().forEach(function(d){
                            if (d.key) {
                                all_possible_values.push(d.key)
                            }
                        });
                        //console.log(all_possible_values);

                        theChart = dc.barChart('#chart-' + name + '-count');
                        theChart
                            .dimension(selectDim)
                            .group(selectDim.group())
                            .x(d3.scaleOrdinal().domain(all_possible_values))
                            .xUnits(dc.units.ordinal)
                            .xAxisLabel(name)
                            .yAxisLabel("Count")
                            .elasticY(true)
                            ;


                        theChart.on('renderlet', function(chart){
                            chart.selectAll("g.x text")
                                //.attr('transform', "rotate(-90)")
                                .style('text-anchor', 'start')
                                .attr('transform', "rotate(-90)")
                                .attr("dx", "+1em")
                                .attr("dy", "-0.2em");
                                //.attr('transform', 'translate(-10,10) rotate(-90)');
                        });

                    }

                }
                else if ($scope.fields[i].type == 'freetext') {
                    console.log('1 Adding: freetext: ', name);

                    var freetextDim = $scope.ndx.dimension(function(d) {return d[name];}); 
                    theChart = dc.textFilterWidget('#chart-' + name + '-count');
                    theChart
                        .dimension(freetextDim);

                    console.log('2 Added: freetext: ', name);
                }

                else {
                    console.log('ALERT!! THIS SHOULD NEVER HAPPEN!!');
                }

                if (!(theChart === undefined)) {
                    d3.selectAll('#' + name + '_reset').on('click', function () {
                        theChart.filterAll();
                        dc.redrawAll();
                    });
                }

                console.log(5);
                //$scope.$apply(function () {dc.renderAll();});
                console.log(6);
            }

            console.log('COMPONENTS: ' + $scope.e_components);

            //If we have 0 charts, do not render anything..
            if ($scope.e_components) {
                console.log(7);

                //Render explore table
                console.log('RENDERING EXPLORE TABLE');
                var dataTable = dc.dataTable('#data-table');

                //Building columns
                var column_functions = [];
                for (var i=0; i<$scope.fields.length; i++) {
                    if ($scope.fields[i].e_order>-1) {
                        var name = $scope.fields[i].name;
                        console.log('Table column: ', name);
                        //column_functions.push(function (d) { return d[name]; }); // This is wrong! it takes always the last value of name

                        if ($scope.fields[i].hasOwnProperty('renderer')) {
                            column_functions.push({
                                label: name,
                                format: $scope.fields[i].renderer
                            });
                        }
                        else {
                            //No renderer
                            column_functions.push(name); // https://dc-js.github.io/dc.js/docs/html/dc.dataTable.html
                        } 
                    }
                }

                dataTable
                    .dimension(allDim)
                    .group(function (d) { return 'dc.js insists on putting a row here so I remove it using JS'; })
                    .size(100)
                    .columns(column_functions)
                    //.columns([function (d) { return d['Chromosome']; }, function (d) { return d['Position']; }])
                    .sortBy(function(d){
                        var c = 1;
                        var p = 1;
                        if (d.hasOwnProperty('Chromosome')) {
                            c = parseInt(d.Chromosome.replace('chr', ''));
                        }
                        if (d.hasOwnProperty('Position')) {
                            p = d.Position;
                        }

                        return (c * 1000000000) + p;

                     })
                    //.order(d3.descending)
                    .on('renderlet', function (table) {
                        // each time table is rendered remove nasty extra row dc.js insists on adding
                        table.select('tr.dc-table-group').remove();
                        // update map with breweries to match filtered data
                    });

                d3.selectAll('#reset_all').on('click', function () {
                    dc.filterAll();
                    dc.renderAll();
                });

                console.log(8);
                var dataCount = dc.dataCount('#data-count');
                dataCount
                    //.dimension(ndx)
                    .dimension($scope.ndx)
                    .group(all);

                console.log(10);

                dc.renderAll();

                dc.chartRegistry.list().forEach(function(chart) {
                    chart.on('filtered', function() {
                        // your event listener code goes here.
                        console.log('FILTERED!'); // https://stackoverflow.com/questions/22392134/is-there-a-way-to-attach-callback-what-fires-whenever-a-crossfilter-dimension-fi 
                    });
                });



                console.log(11);
            }
        }; // End of function

    // select explore changed
    $scope.e_select_changed = function() {
        //e_selected.selected point to the fields record
        //Choose bin size

        //console.log('table_data:')
        //console.log($scope.table_data);

        //var sample_data = [{Bases:1}, {Bases:2}, {Bases:3}, {Bases:4}, {Bases:5}];

        //What is the maximum e_order?
        var max_i = -1;
        for (var i=0; i<$scope.fields.length; i++) {
            if ($scope.fields[i].e_order > max_i) {
                max_i = $scope.fields[i].e_order;
            }
        }

        console.log('Max i:');
        console.log(max_i);

        //Change the order of the selected field
        $scope.e_selected.selected.e_order = max_i+1;
        console.log('Assign ' + $scope.e_selected.selected.name + '  e_order : ' + $scope.e_selected.selected.e_order);

        //Reorder explore charts
        $scope.explore_selected();

        $scope.e_selected.selected = undefined; //Remove the selected.

        //$scope.$apply(function () {
        //    $scope.render_crossfilter();
        //});
        //$timeout(function(){$scope.render_crossfilter();}, 1000);  //TODO https://stackoverflow.com/questions/15207788/calling-a-function-when-ng-repeat-has-finished 
    };

    $scope.$on('test', function(ngRepeatFinishedEvent) {
        console.log("ddddone");
        $scope.render_crossfilter();
    });

    //End of explore

});














































































































































































































































































































































































































































































