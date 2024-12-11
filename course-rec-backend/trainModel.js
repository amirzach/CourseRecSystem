const { DecisionTreeClassifier } = require("ml-cart");
const Grade = require("./models/Grade");

let decisionTree;

const trainModel = async () => {
  const data = await Grade.find({});
  if (data.length === 0) return null;

  const features = data.map((entry) => {
    const { recommendedCourse, ...grades } = entry.toObject();
    return { input: grades, output: recommendedCourse };
  });

  const inputs = features.map((f) => Object.values(f.input));
  const outputs = features.map((f) => f.output);

  decisionTree = new DecisionTreeClassifier();
  decisionTree.train(inputs, outputs);

  return decisionTree;
};

const predictCourse = (grades) => {
  if (!decisionTree) throw new Error("Model not trained yet!");
  const prediction = decisionTree.predict(Object.values(grades));
  const confidence = decisionTree.getConfidence(Object.values(grades));
  return { prediction, confidence };
};

module.exports = { trainModel, predictCourse };
