from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import modules
from modules.bhulekh_integration import BhulekhIntegration
from modules.ocr_processor import OCRProcessor
from modules.blockchain_service import BlockchainService
from modules.dispute_predictor import DisputePredictor
from modules.ar_service import ARService
from modules.multi_state_search import MultiStateSearch
from modules.zero_knowledge_proofs import ZeroKnowledgeProofs

# Initialize services
bhulekh = BhulekhIntegration()
ocr_processor = OCRProcessor()
blockchain = BlockchainService()
dispute_predictor = DisputePredictor()
ar_service = ARService()
multi_state_search = MultiStateSearch()
zkp = ZeroKnowledgeProofs()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/search/land', methods=['POST'])
def search_land():
    """Multi-state land search endpoint"""
    try:
        data = request.json
        state = data.get('state', 'bihar')
        district = data.get('district')
        village = data.get('village')
        khasra_no = data.get('khasra_no')
        
        # Search land records
        results = bhulekh.search_land_records(state, district, village, khasra_no)
        
        # Log query to blockchain
        tx_hash = blockchain.log_land_query(data)
        results['blockchain_tx'] = tx_hash
        
        return jsonify({
            'success': True,
            'data': results,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Land search error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/search/multi-state', methods=['POST'])
def search_multi_state():
    """Multi-state land search endpoint"""
    try:
        data = request.json
        states = data.get('states', ['bihar'])
        search_type = data.get('search_type', 'khasra')
        search_value = data.get('search_value')
        
        # Perform multi-state search
        results = multi_state_search.search_across_states(data)
        
        # Log query to blockchain
        tx_hash = blockchain.log_land_query(data)
        results['blockchain_tx'] = tx_hash
        
        return jsonify({
            'success': True,
            'data': results,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Multi-state search error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/search/supported-states', methods=['GET'])
def get_supported_states():
    """Get list of supported states for multi-state search"""
    try:
        states = multi_state_search.get_supported_states()
        return jsonify({
            'success': True,
            'states': states,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting supported states: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/upload/deed', methods=['POST'])
def upload_deed():
    """Upload and process Kaithi deed using OCR"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Process deed with OCR
        ocr_results = ocr_processor.process_deed(file)
        
        # Extract land details
        land_details = ocr_processor.extract_land_details(ocr_results)
        
        # Predict dispute probability
        dispute_score = dispute_predictor.predict_dispute(land_details)
        
        # Log to blockchain
        tx_hash = blockchain.log_deed_upload(land_details, dispute_score)
        
        return jsonify({
            'success': True,
            'ocr_results': ocr_results,
            'land_details': land_details,
            'dispute_score': dispute_score,
            'blockchain_tx': tx_hash,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Deed upload error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ar/geo-overlay', methods=['POST'])
def get_geo_overlay():
    """Get AR geo-overlay data for land verification"""
    try:
        data = request.json
        land_id = data.get('land_id')
        coordinates = data.get('coordinates')
        
        # Generate AR overlay data
        ar_data = ar_service.generate_geo_overlay(land_id, coordinates)
        
        return jsonify({
            'success': True,
            'ar_data': ar_data,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"AR overlay error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/alerts/smart', methods=['GET'])
def get_smart_alerts():
    """Get smart alerts for land disputes and updates"""
    try:
        user_id = request.args.get('user_id')
        alerts = dispute_predictor.get_smart_alerts(user_id)
        
        return jsonify({
            'success': True,
            'alerts': alerts,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Smart alerts error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/blockchain/verify', methods=['POST'])
def verify_blockchain():
    """Verify land record on blockchain"""
    try:
        data = request.json
        land_id = data.get('land_id')
        tx_hash = data.get('tx_hash')
        
        verification = blockchain.verify_land_record(land_id, tx_hash)
        
        return jsonify({
            'success': True,
            'verification': verification,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Blockchain verification error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/zkp/create-ownership-proof', methods=['POST'])
def create_ownership_proof():
    """Create zero-knowledge proof for land ownership"""
    try:
        data = request.json
        land_data = data.get('land_data')
        owner_identity = data.get('owner_identity')
        
        proof_result = zkp.create_land_ownership_proof(land_data, owner_identity)
        
        return jsonify({
            'success': True,
            'proof': proof_result,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"ZKP ownership proof error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/zkp/verify', methods=['POST'])
def verify_zkp():
    """Verify zero-knowledge proof"""
    try:
        data = request.json
        proof_id = data.get('proof_id')
        verifier_type = data.get('verifier_type', 'verifier')
        
        verification = zkp.verify_proof(proof_id, verifier_type)
        
        return jsonify({
            'success': True,
            'verification': verification,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"ZKP verification error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/zkp/anonymous-query', methods=['POST'])
def create_anonymous_query():
    """Create anonymous query with zero-knowledge proof"""
    try:
        data = request.json
        query_params = data.get('query_params')
        user_salt = data.get('user_salt')
        
        proof_result = zkp.create_anonymous_query_proof(query_params, user_salt)
        
        return jsonify({
            'success': True,
            'anonymous_proof': proof_result,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Anonymous query proof error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/demo/complete-workflow', methods=['POST'])
def demo_complete_workflow():
    """Complete demo workflow: deed upload -> analysis -> AR map"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        # Step 1: Process deed with OCR
        ocr_results = ocr_processor.process_deed(file)
        land_details = ocr_processor.extract_land_details(ocr_results)
        
        # Step 2: Predict disputes
        dispute_score = dispute_predictor.predict_dispute(land_details)
        
        # Step 3: Search existing records
        search_results = bhulekh.search_land_records(
            land_details.get('state', 'bihar'),
            land_details.get('district'),
            land_details.get('village'),
            land_details.get('khasra_no')
        )
        
        # Step 4: Generate AR overlay
        ar_data = ar_service.generate_geo_overlay(
            land_details.get('land_id'),
            land_details.get('coordinates')
        )
        
        # Step 5: Log everything to blockchain
        tx_hash = blockchain.log_complete_workflow(land_details, dispute_score, search_results)
        
        return jsonify({
            'success': True,
            'workflow_complete': True,
            'steps_completed': ['ocr_processing', 'dispute_prediction', 'land_search', 'ar_generation', 'blockchain_logging'],
            'results': {
                'ocr_results': ocr_results,
                'land_details': land_details,
                'dispute_score': dispute_score,
                'search_results': search_results,
                'ar_data': ar_data,
                'blockchain_tx': tx_hash
            },
            'processing_time': '2 minutes',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Demo workflow error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
