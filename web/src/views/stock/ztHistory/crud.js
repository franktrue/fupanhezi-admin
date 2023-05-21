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
            title: '封板金额',
            key: 'fb_amount',
            type: "number",
            formatter: (row, column, cellValue) => {
              return vm.$util.num2human(cellValue)
            },
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
              rules: [{ required: true, message: '封板金额必填' }]
            }
          },
          {
            title: '首次封板时间',
            key: 'first_zt_time',
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '最后封板时间',
            key: 'last_zt_time',
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '开板次数',
            key: 'zb_num',
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
            title: '涨停统计',
            key: 'zt_statistics',
            form: {
              component: {
                props: {
                  clearable: true
                }
              }
            }
          },
          {
            title: '连板天数',
            key: 'ztlb_num',
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
            title: '排序',
            key: 'sort',
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
            title: '真实流通市值',
            key: 'zs_sz',
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
            title: '真实换手率（%）',
            key: 'real_hs_rate',
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
            title: '市盈率（%）',
            key: 'pe',
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
            title: '涨停类型',
            key: 'zt_type',
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
            title: '涨停原因',
            key: 'zt_reason',
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
