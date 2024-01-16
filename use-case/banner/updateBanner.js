/**
 *updateBanner.js
 */

const  bannerEntity = require('../../entities/banner');
const response = require('../../utils/response');

/**
 * @description : update record with data by id.
 * @param {Object} params : request body including query and data.
 * @param {Object} req : The req object represents the HTTP request.
 * @param {Object} res : The res object represents HTTP response.
 * @return {Object} : updated Banner. {status, message, data}
 */
const updateBanner = ({
  bannerDb, updateValidation
}) => async (params,req,res) => {
  let {
    dataToUpdate, query 
  } = params;
  const validateRequest = await updateValidation(dataToUpdate);
  if (!validateRequest.isValid) {
    return response.validationError({ message : `Invalid values in parameters, ${validateRequest.message}` });
  }
  let banner = bannerEntity(dataToUpdate);
  banner = await bannerDb.updateOne(query,banner);
  if (!banner){
    return response.recordNotFound();
  }
  return response.success({ data:banner });
};
module.exports = updateBanner;