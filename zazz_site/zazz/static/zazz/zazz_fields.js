
global_fields = [
{'name': 'Chromosome', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 1 },
{'name': 'Type', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 2 },
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
            }, 'xUnits': 20, 'order': 3 },
{'name': 'Location', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'normal', 'itemArray': [], 'selected2': ['ALL'], 'order': 4 },
{'name': 'Reference', 'type': 'freetext', 'selected': false, 'e_order': -1, 'database': 'normal', 'text' : '', 'order': 5 },
{'name': 'Length', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
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
            }, 'xUnits': 20, 'order': 6 },
{'name': 'Genotype', 'type': 'freetext', 'selected': false, 'e_order': -1, 'database': 'normal', 'text' : '', 'order': 7 },
{'name': 'PValue', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
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
            }, 'xUnits': 20, 'order': 8 },
{'name': 'Coverage', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
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
            }, 'xUnits': 20, 'order': 9 },
{'name': 'Allele_Coverage_1', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
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
            }, 'xUnits': 20, 'order': 10 },
{'name': 'Allele_Coverage_2', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
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
            }, 'xUnits': 20, 'order': 11 },
{'name': 'MAF', 'type': 'slider', 'selected': false, 'e_order': -1, 'database': 'normal', 'slider': {
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
            }, 'order': 12 },
{'name': 'Gene', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi', 'itemArray': [], 'selected2': ['ALL'], 'table': 'Transcripts', 'order': 13 },
{'name': 'Transcript', 'type': 'checkbox', 'selected': false, 'e_order': -1, 'database': 'multi', 'itemArray': [], 'selected2': ['ALL'], 'table': 'Transcripts', 'order': 14 }
];

