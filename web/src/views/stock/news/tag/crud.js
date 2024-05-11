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
      width: '60%'
    },
    columns: [
      {
        title: '名称',
        key: 'name',
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
        title: '简介',
        key: 'desc',
        type: 'textarea',
        form: {
          component: {
            placeholder: '请输入简介',
            showWordLimit: true,
            maxlength: '500',
            props: {
              type: 'textarea'
            }
          }
        }
      },
      {
        title: '成分股',
        key: 'cons',
        show: false,
        type: 'select',
        dict: {
          url(dict,{form,component}){
            console.log(form)
            return '/api/stock/history/dict/'
          },
          cache: false,
          onReady:(data,dict,options)=>{
            vm.optionData = data
            vm.formOption = options
          },
        },
        form: {
          component: {
            props: {
              separator: ',' ,//多选时，value的分隔符
              elProps:{
                filterable: true,
                multiple: true,
                clearable: true,
                filterMethod: function(val) {
                  if(val) {
                    const arr = []
                    vm.optionData.forEach((item) => {
                      if(val.includes(item.value.substring(0,6))) {
                        arr.push(item.value)
                      }
                    })
                    if (arr.length>0) {
                      vm.formOption.form.cons = arr
                    } else {
                      this.$options.parent.dictOptions = vm.optionData.filter((item) => {
                        return item.value.includes(val)
                      })
                    }
                  } else {
                    this.$options.parent.dictOptions = vm.optionData
                  }
                }
              },
            },
            on:{ //除input change事件外，更多组件事件监听
              change(event){
                let include_stocks = event.scope.form.include_stocks
                let tmp = {}
                for (let stock of event.event) {
                  tmp[stock] = include_stocks[stock] || ""
                }
                event.scope.form.include_stocks = tmp
              }
            },
          }
        },
        valueBuilder (row,key) {
          let include_stocks = JSON.parse(row.include_stocks)
          let cons = []
          for (let key in include_stocks) {
            cons.push(key)
          }
          row.cons = cons
        },
        valueResolve (row,key) {
          if (row.cons !=null && row.cons.length>0) {
            const result = row.cons.map(item => {
              const [stock_code, stock_name] = item.split(' ');
              return { stock_code, stock_name};
            });
            row.cons = result
          }
        },
      },
      {
        title : '关联根据',
        key : 'include_stocks',
        show: false,
        form: {
          value: {},
          slot : true
        },
        valueBuilder (row,key) {
          row.include_stocks = JSON.parse(row.include_stocks)
        },
        valueResolve (row,key) {
          row.include_stocks = JSON.stringify(row.include_stocks)
        },
      },
      {
        title: '排序',
        key: 'sort',
        width: 50,
        type: "number",
        form: {
          value: 0,
          component: {
            props: {
              clearable: true
            }
          },
          rules: [{ required: true, message: '序号必填' }]
        }
      },
    ]
  }
}
