import { Component, onWillStart, useState, useSubEnv,xml } from "@odoo/owl";
import { Dialog } from '@web/core/dialog/dialog';
import { _t } from "@web/core/l10n/translation";
import { rpc } from "@web/core/network/rpc";
import { formatCurrency } from '@web/core/currency';

 var xml_template = xml`
        <Dialog size="props.size" title="title" >
        <div style="display: grid;grid-auto-flow: column;justify-content: start;column-gap: 200px;">
            <div  style="width: 150px;">
                <span>Node Name:</span> <div t-esc="props.api_node_engine_name"/>
                Description : <div> <t t-esc="state.description"/></div>
            </div>
            <div  style="width:150px;">
                <img
                    t-attf-src="/web/image/product.product/{{props.product_id}}/image_256"
                    alt="Product Image"
                    role="img"
                    class="img-thumbnail rounded"
                />
            </div>
           </div>
           <t t-foreach="state.parameters" t-as="api_param" t-key="api_param">
                <div>
                    <t t-if="state.parameters_type[api_param]=='COMBO'">
                        <div>
                            <span style="width:100px;" t-esc="state.parameters.get(api_param)"/>:
                            <select  
                                style="width:100px;"
                                t-model="state.parameters_value[api_param]"
                                t-on-change="(ev) => this.onParameterChange(ev.target.value)">
                                <t t-foreach="state.parameters_values[api_param]" t-as="api_param_value" t-key="api_param_value">
                                    <option t-att-value="api_param_value"><span t-esc="api_param_value"/></option>
                                </t>
                            </select>
                        </div>
                    </t>
                    <t t-else="">
                    <span t-esc="state.parameters.get(api_param)"/>:
                    <input  
                        t-model.number="state.parameters_value[api_param]" 
                        t-att-title="state.parameters_title.get(api_param)"
                        t-on-change="(ev) => this.onParameterChange(ev.target.value)"
                        />
                    </t>
                </div>
            </t>
             <footer>
                <button
                    name="api_product_configurator_confirm_button"
                    class="btn btn-primary order-2 order-md-1"
                    t-on-click="onConfirm">
                    Confirm
                </button>
                <button
                    name="api_product_configurator_cancel_button"
                    class="btn btn-secondary order-2 order-md-1"
                    t-on-click="onDiscard">
                    Cancel
                </button>
                <button
                    name="api_product_configurator_show_web_model_button"
                    class="btn btn-secondary order-2 order-md-1"
                    t-on-click="show_web_model">
                    Show 3D
                </button>
             </footer>
        </Dialog>
    `;


export class ApiProductConfiguratorDialog extends Component {
    static template = xml_template;
    static components = { Dialog};
    static description = "Api Dialog ";
    static props = {
        close: { type: Function },
        save: { type: Function },
        api_configurator_value:'',
        api_node_engine_name:{type: String},
        product_id:{type: Number},
    };
    
    setup() {
       this.title = _t("Configure your product");
       this.url_create_web_model = '/plm_api/product_configurator/create_web_model';
       this.url_get_indipendent_parameter = '/plm_api/product_configurator/get_indipendent_parameter';
       //
       this.state = useState({parameters: new Map(),
                              parameters_value: new Object(),
                              parameters_title: new Map(),
                              parameters_type: new Object(),
                              parameters_values: new Object(),
                              description:'',
                              });

       onWillStart(async () => {
           const ret = await rpc(this.url_get_indipendent_parameter,
                            {product_id:this.props.product_id}); 
           for (var key in ret) {
            if (ret.hasOwnProperty(key)) {
               if (ret[key][2].length>0){
                   this.state.parameters_type[key]='COMBO';
               } else {
                   this.state.parameters_type[key]='IMPUT';
               }
               this.state.parameters_values[key] = ret[key][2];
               this.state.parameters_value[key]=ret[key][1];
               this.state.parameters.set(key, ret[key][3]);
               this.state.parameters_title.set(key, ret[key][4]);
               }
           }
       });
   };
   
   onParameterChange(newName) {
        console.log("perform api computation");
        console.log(this.state.parameters_value);
        var attr_name = ''
        for (var key in this.state.parameters_value) {
            attr_name = attr_name + "\n" + key + ":" + this.state.parameters_value[key];
            }
        this.state.description=attr_name;
        
   };
   async show_web_model(){
        const ret = await rpc(this.url_create_web_model,
                              {product_id:this.props.product_id,
                              parameters: this.state.parameters_value}); 
        console.log(ret);
        if (ret.message){
            alert(ret.message);
        }
        if (ret.url){
              window.open(ret.url, '_blank').focus();
        }
       
   }
   async _loadData(onlyMainProduct) {
   }
   /*
    * Confirm the current combination(s).
    *
    * @return {undefined}
    */
   async onConfirm(options) {
        await this.props.save(
            this.state.parameters_value,
            options,
        );
        this.props.close();
   }
   /*
    * Discard the modal.
    */
   onDiscard() {
        this.props.close();
   }
    /*
    * Hook to append additional RPC params in overriding modules.
    *
    * @return {Object} - The additional RPC params.
    */
   _getAdditionalRpcParams() {
       return {};
   }
   close(){
       
   };
   save(){
       
   };
   discard(){
       
   };
}