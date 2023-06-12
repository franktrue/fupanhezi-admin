export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      rowId: 'id',
      height: '100%', // 表格高度100%, 使用toolbar必须设置
      border: false
    },
    rowHandle: {
      width: 140,
      view: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      edit: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      }
    },
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      appendToBody: true, // 子表格必须 否则弹出对话框无法显示最顶层
      defaultSpan: 24, // 默认的表单 span
      width: '35%'
    },
    columns: [
      {
        title: "日期",
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
        title: '指数代码',
        key: 'name',
        show: false,
        type: 'input',
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '代码必填项' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入代码'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '名称',
        key: 'name',
        show: false,
        type: 'input',
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '名称必填项' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入名称'
          },
          itemProps: {
            class: { yxtInput: true }
          }
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
        show: false,
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
        show: false,
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
        formatter: (row, column, cellValue) => {
          return cellValue + '/'+row.close_pe+'%'
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
          rules: [{ required: true, message: '收盘价必填' }]
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
        title: '收盘%',
        key: 'close_pe',
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
      }
    ]
  }
}
