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
          },
          custom: [{
            text: '营业部',
            type: 'success',
            size: 'small',
            icon: 'el-icon-folder',
            emit: 'officeItem'
          }]
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
            title: "上榜日",
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
                { required: true, message: "上榜日必填" }
              ],
              component: {
                props: {
                  clearable: true,
                  format: 'yyyy-MM-dd',
                  valueFormat: 'yyyy-MM-dd'
                },
                placeholder: "请输入上榜日"
              }
            }
          },
          {
            fixed: 'left',
            title: '序号',
            key: 'serial',
            type: "number",
            form: {
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '序号必填' }]
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
            search: true,
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
            title: '解读',
            key: 'interpretation',
            type: "number",
            form: {
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '解读必填' }]
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
            title: '涨跌幅%',
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
            title: '龙虎榜净买额',
            key: 'lhb_net_buy_amo',
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
            title: '龙虎榜买入额',
            key: 'lhb_buy_amo',
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
            title: '龙虎榜卖出额',
            key: 'lhb_sell_amo',
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
            title: '龙虎榜成交额',
            key: 'lhb_amo',
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
            title: '市场总成交额',
            key: 'market_total_amo',
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
            title: '净买额占总成交比%',
            key: 'net_buy_amo_pe',
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
            title: '成交额占总成交比%',
            key: 'amo_pe',
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
            title: '换手率%',
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
            title: '流通市值',
            key: 'circulate_market_value',
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
            title: '上市原因',
            key: 'rank_reson',
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
