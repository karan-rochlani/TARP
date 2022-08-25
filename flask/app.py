from flask import Flask,render_template,url_for,request,session,logging,redirect,flash
import os
import main
from flask import jsonify
app = Flask(__name__)


@app.route('/encryption',methods = ['POST', 'GET']) 
def encryption():      
  if request.method == 'POST':
        result = request.get_json()
        print(result)
        image = result['path']
        # print(path)
        encrypted_image,mask,shape, enc_rel_path = main.encryption(image)
        new_result={
          'encrypted_image':encrypted_image,
          'mask':mask,
          'shape':shape,
          'enc_rel_path': enc_rel_path
        }
        return jsonify(new_result)

  
@app.route('/decryption', methods = ['POST', 'GET'])
def decryptiom():
  if request.method == 'POST':
        result = request.get_json()
        print(result)
        image = result['encrypted_image']
        mask=result['mask']
        shape=result['shape']
        decrypted_image, dec_rel_path = main.decryption(image,mask,shape)
        new_result={
          'decrypted_image':decrypted_image,
          'dec_rel_path': dec_rel_path
        }
        return jsonify(new_result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)