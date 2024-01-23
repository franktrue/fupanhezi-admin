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
        fixed: 'left',
        title: '排序',
        key: 'sort',
        width: 50,
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
        title: '营业部名称',
        key: 'office',
        width: 200,
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
        type: 'input',
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '营业部名称必填项' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入营业部名称'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '买入金额',
        key: 'buy_amount',
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
        title: '买入占比',
        key: 'buy_rate',
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
        title: '卖出金额',
        key: 'sell_amount',
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
        title: '卖出占比',
        key: 'sell_rate',
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
        title: '净额',
        key: 'net_amount',
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
        title: '类型',
        key: 'type',
        type: 'radio',
        search: { disabled: false, component: { name: 'dict-select', props: { clearable: true } } },
        dict: {
          data: vm.dictionary('stock_option_type')
        },
        form: {
          value: 0,
          component: {
            props: {
              clearable: true
            }
          },
          helper: "买/卖前5"
        }
      }
    ]
  }
}
