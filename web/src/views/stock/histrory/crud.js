export const crudOptions = vm => {
  return {
      pageOptions: {
          compact: true
      },
      options: {
          tableType: "vxe-table",
          rowKey: true, // 必须设置，true or false
          rowId: "id",
          height: "100%", // 表格高度100%, 使用toolbar必须设置
          highlightCurrentRow: false
      },
      rowHandle: {
          width: 140,
          view: {
              thin: true,
              text: "",
              disabled() {
                  return !vm.hasPermissions("Retrieve");
              }
          },
          edit: {
              thin: true,
              text: "",
              disabled() {
                  return !vm.hasPermissions("Update");
              }
          },
          remove: {
              thin: true,
              text: "",
              disabled() {
                  return !vm.hasPermissions("Delete");
              }
          }
      },
      indexRow: false,
      viewOptions: {
          componentType: "form"
      },
      formOptions: {
          defaultSpan: 24, // 默认的表单 span
          width: "35%"
      },
      columns: [
          {
            fixed: 'left',
            title: "交易日期",
            key: "date",
            type: "date",
            search: {
              component: {
                props: {
                  format: 'yyyy-MM-dd',
                  valueFormat: 'yyyy-MM-dd'
                }
              }
            },
            form: {
              rules: [
                { required: true, message: "交易日期必填" }
              ],
              component: {
                props: {
                  clearable: true,
                  format: 'yyyy-MM-dd',
                  valueFormat: 'yyyy-MM-dd'
                },
                placeholder: "请输入交易日期"
              }
            }
          },
          {
            fixed: 'left',
            title: '股票代码',
            key: 'stock_code',
            search: {
              component: {
                props: {
                  clearable: true
                }
              }
            },
            form: {
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '股票代码必填' }]
            }
          },
          {
            fixed: 'left',
            title: '股票名称',
            key: 'stock_name',
            search: {
              component: {
                props: {
                  clearable: true
                }
              }
            },
            form: {
              component: {

                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '股票名称必填' }]
            }
          },
          {
            title: '开盘价',
            key: 'open',
            type: "number",
            form: {
              component: {
                name: 'el-input-number',
                props: {
                  precision: 2
                }
              },
              scopedSlots: {
                prefix: () => '￥'
              },
              rules: [{ required: true, message: '开盘价必填' }]
            }
          },
          {
            title: '最高价',
            key: 'high',
            type: "number",
            form: {
              component: {
                name: 'el-input-number',
                props: {
                  precision: 2
                }
              },
              scopedSlots: {
                prefix: () => '￥'
              },
              rules: [{ required: true, message: '最高价必填' }]
            }
          },
          {
            title: '最低价',
            key: 'low',
            type: "number",
            form: {
              component: {
                name: 'el-input-number',
                props: {
                  precision: 2
                }
              },
              scopedSlots: {
                prefix: () => '￥'
              },
              rules: [{ required: true, message: '最低价必填' }]
            }
          },
          {
            title: '收盘价',
            key: 'close',
            type: "number",
            form: {
              component: {
                name: 'el-input-number',
                props: {
                  precision: 2
                }
              },
              scopedSlots: {
                prefix: () => '￥'
              },
              rules: [{ required: true, message: '收盘价必填' }]
            }
          },
          {
            title: '昨日收盘',
            key: 'pre_close',
            type: "number",
            form: {
              component: {
                name: 'el-input-number',
                props: {
                  precision: 2
                }
              },
              scopedSlots: {
                prefix: () => '￥'
              },
              rules: [{ required: true, message: '昨日收盘价必填' }]
            }
          },
          {
            title: '成交量',
            key: 'vol',
            type: 'number',
            formatter: (row, column, cellValue) => {
              return vm.$util.num2human(cellValue)
            },
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '成交额',
            key: 'amo',
            type: 'number',
            formatter: (row, column, cellValue) => {
              return vm.$util.num2human(cellValue)
            },
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '换手率（%）',
            key: 'hs_rate',
            type: 'number',
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '涨跌幅',
            key: 'change_amo',
            type: 'number',
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '开盘%',
            key: 'open_pe',
            type: 'number',
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '最高%',
            key: 'high_pe',
            type: 'number',
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '最低%',
            key: 'low_pe',
            type: 'number',
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '收盘%',
            key: 'close_pe',
            type: 'number',
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '总市值',
            key: 'z_sz',
            type: 'number',
            formatter: (row, column, cellValue) => {
              return vm.$util.num2human(cellValue)
            },
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '流通市值',
            key: 'lt_sz',
            show: false,
            type: 'number',
            formatter: (row, column, cellValue) => {
              return vm.$util.num2human(cellValue)
            },
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '市盈率',
            key: 'pe',
            show: false,
            type: 'number',
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '竞价金额',
            key: 'auction_amo',
            type: 'number',
            formatter: (row, column, cellValue) => {
              return vm.$util.num2human(cellValue)
            },
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '竞价量',
            key: 'auction_vol',
            type: 'number',
            formatter: (row, column, cellValue) => {
              return vm.$util.num2human(cellValue)
            },
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '竞价未匹配金额',
            key: 'auction_no_match_amo',
            show: false,
            type: 'number',
            formatter: (row, column, cellValue) => {
              return vm.$util.num2human(cellValue)
            },
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '竞价未匹配量',
            key: 'auction_no_match_vol',
            show: false,
            type: 'number',
            formatter: (row, column, cellValue) => {
              return vm.$util.num2human(cellValue)
            },
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '竞价异动类型',
            key: 'auction_type',
            show: false,
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '竞价异动说明',
            key: 'auction_explain',
            show: false,
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '是否龙虎榜',
            key: 'is_lhb',
            type: 'radio',
            search: { disabled: false, component: { name: 'dict-select', props: { clearable: true } } },
            dict: {
              data: vm.dictionary('button_whether_number')
            },
            form: {
              value: 0,
              component: {
                props: {
                  clearable: true
                }
              }
            },
            component:{ //单元格 使用value格式化组件，展示为tag
              name:'values-format'
            }
          },
          {
            title: '上榜原因',
            key: 'lhb_reson',
            show: false,
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '上榜分析',
            key: 'lhb_parse',
            show: false,
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
      ]
  };
};
