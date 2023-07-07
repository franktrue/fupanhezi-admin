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
        title: '板块代码',
        key: 'code',
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
            { required: true, message: '板块代码必填项' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入板块代码'
          }
        }
      },
      {
        title: '板块名称',
        key: 'board_name',
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
            { required: true, message: '板块名称必填项' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入板块名称'
          }
        }
      },
      {
        title: '股票代码',
        key: 'stock_code',
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
            { required: true, message: '股票代码必填项' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入股票代码'
          }
        }
      },
      {
        title: '股票名称',
        key: 'stock_name',
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
            { required: true, message: '股票名称必填项' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入股票名称'
          }
        }
      },
      {
        title: '类型',
        key: 'type',
        type: 'radio',
        search: {
          disabled: false
        },
        dict:  {
          data: [
            {"value": "concept", "label": "概念"},
            {"value": "industry", "label": "行业"},
            {"value": "sub_concept", "label": "子题材"},
          ]
        },
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '类型必选' }
          ]
        }
      },
      {
        title: '解析',
        key: 'brief',
        type: 'textarea',
        show: false,
        form: {
          component: {
            placeholder: '请输入解析',
            showWordLimit: true,
            maxlength: '500',
            props: {
              type: 'textarea'
            }
          }
        }
      },
    ]
  }
}
