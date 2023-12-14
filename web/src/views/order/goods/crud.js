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
            title: '名称',
            key: 'name',
            type: "input",
            search: true,
            form: {
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '名称必填' }]
            }
          },
          {
            title: '产品 ID',
            key: 'product_id',
            type: "input",
            search: true,
            form: {
              component: {
                props: {
                  clearable: true,
                }
              },
              rules: [{ required: true, message: '产品 ID必填' }],
              helper: '对应AppStore内置购买项目产品ID，仅IOS内有效'
            }
          },
          {
            title: '是否体验卡',
            key: 'is_try',
            type: 'dict-switch',
            search: {
              disabled: true
            },
            dict: {
              data: vm.dictionary('button_whether_bool')
            },
            form: {
              value: false,
              component: {
                placeholder: '请选择是否目录'
              },
              helper: "体验卡仅可购买一次且无法分佣"
            }
          },
          {
            title: '有效期（年）',
            key: 'year_num',
            type: 'number',
            form: {
              value: 0,
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '有效期必填' }]
            }
          },
          {
            title: '有效期（月）',
            key: 'month_num',
            type: 'number',
            form: {
              value: 0,
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '有效期必填' }]
            }
          },
          {
            title: '有效期（日）',
            key: 'day_num',
            type: 'number',
            form: {
              value: 0,
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '有效期必填' }]
            }
          },
          {
            title: '市场价',
            key: 'sales_price',
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
              rules: [{ required: true, message: '市场价必填' }]
            }
          },
          {
            title: '售价',
            key: 'payment_price',
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
              rules: [{ required: true, message: '支付价' }]
            }
          },
          {
            title: '对应等级',
            key: 'level',
            type: "number",
            form: {
              value: 1,
              component: {
                name: 'el-input-number',
              },
              rules: [{ required: true, message: '对应等级必填' }],
              helper: "用户默认等级为1级"
            }
          },
          {
            title: '销量',
            key: 'sale_num',
            type: "number",
            form: {
              disabled: true
            }
          },
          {
            title: '备注',
            key: 'remark',
            type: "textarea",
            form: {
              component: {
                placeholder: '请输入备注',
                showWordLimit: true,
                maxlength: '500',
                props: {
                  type: 'textarea'
                }
              }
            }
          },
          {
            title: '是否下架',
            key: 'del_flag',
            type: 'dict-switch',
            search: { disabled: false, component: { name: 'dict-select', props: { clearable: true } } },
            dict: {
              data: vm.dictionary('button_whether_bool')
            },
            form: {
              value: false,
              component: {
                props: {
                  clearable: true
                }
              },
              rules: [{ required: true, message: '是否支付必填' }],
              helper: "下架后产品用户不可见"
            }
          }
      ]
  };
};
