

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


CREATE DATABASE IF NOT EXISTS esd_db DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

GRANT ALL PRIVILEGES ON esd_db.* TO 'esd_user'@'%' WITH GRANT OPTION;

USE esd_db;
--
-- Database: `esd_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `Bubble`
--

DROP TABLE IF EXISTS `Bubble`;
CREATE TABLE IF NOT EXISTS `Bubble` (
  `bubble_id` int(255) NOT NULL,
  `bubble_name` varchar(255) NOT NULL,
  `create_timestamp` int(255) NOT NULL,
  `meet_timestamp` int(255) NOT NULL,
  `capacity` int(255) NOT NULL,
  `agenda` varchar(255) NOT NULL,
  `module_code` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Bubble`
--

INSERT INTO `Bubble` (`bubble_id`, `bubble_name`, `create_timestamp`, `meet_timestamp`, `capacity`, `agenda`, `module_code`) VALUES
(1, 'IS111 Workshop', 1619798400, 1619798400, 20, 'Recap on dictionaries', 'IS111'),
(2, 'IS210 Workshop', 1619798400, 1619798400, 20, 'How to draw workflow diagrams', 'IS210');

-- --------------------------------------------------------

--
-- Table structure for table `BubbleComment`
--

DROP TABLE IF EXISTS `BubbleComment`;
CREATE TABLE IF NOT EXISTS `BubbleComment` (
  `bubble_id` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `timestamp` int(255) NOT NULL,
  `comment` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `BubbleComment`
--

INSERT INTO `BubbleComment` (`bubble_id`, `email`, `timestamp`, `comment`) VALUES
('1', 'b@gmail.com', 1619798400, 'This app is amazing.'),
('1', 'p@gmail.com', 1619798402, 'I think so too!'),
('2', 'p@gmail.com', 1619798401, 'This app is amazing.');

-- --------------------------------------------------------

--
-- Table structure for table `BubbleFile`
--

DROP TABLE IF EXISTS `BubbleFile`;
CREATE TABLE IF NOT EXISTS `BubbleFile` (
  `bubble_id` int(255) NOT NULL,
  `timestamp` int(255) NOT NULL,
  `s3_bucket` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `BubbleFile`
--

INSERT INTO `BubbleFile` (`bubble_id`, `timestamp`, `s3_bucket`) VALUES
(1, 1619798400, '#'),
(2, 1619798401, '#');

-- --------------------------------------------------------

--
-- Table structure for table `BubbleRole`
--

DROP TABLE IF EXISTS `BubbleRole`;
CREATE TABLE IF NOT EXISTS `BubbleRole` (
  `bubble_id` int(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `role` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `BubbleRole`
--

INSERT INTO `BubbleRole` (`bubble_id`, `email`, `role`) VALUES
(1, 'b@gmail.com', 'mentor'),
(1, 'p@gmail.com', 'participant'),
(2, 'b@gmail.com', 'participant'),
(2, 'p@gmail.com', 'mentor');

-- --------------------------------------------------------

--
-- Table structure for table `Log`
--

DROP TABLE IF EXISTS `Log`;
CREATE TABLE IF NOT EXISTS `Log` (
  `email` varchar(255) NOT NULL,
  `timestamp` int(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `json_data_string` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Log`
--

INSERT INTO `Log` (`email`, `timestamp`, `type`, `json_data_string`) VALUES
('b@gmail.com', 1619798400, 'log', '{message: \"hello world\"');

-- --------------------------------------------------------

--
-- Table structure for table `Module`
--

DROP TABLE IF EXISTS `Module`;
CREATE TABLE IF NOT EXISTS `Module` (
  `module_code` varchar(255) NOT NULL,
  `module_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Module`
--

INSERT INTO `Module` (`module_code`, `module_name`) VALUES
('ACCT001', 'Accounting Study Mission (Asian Studies)(Taiwan)'),
('ACCT007', 'Applied Governance and Risk Management for Student Organizations(SMU-X)'),
('ACCT101', 'Financial Accounting'),
('ACCT102', 'Management Accounting'),
('ACCT105', 'Financial Accounting for Law'),
('ACCT201', 'Corporate Reporting and Financial Analysis'),
('ACCT221', 'Accounting Information Systems'),
('ACCT223', 'Taxation'),
('ACCT224', 'Financial Reporting and Analysis'),
('ACCT331', 'Audit and Assurance'),
('ACCT332', 'Accounting Thought and Governance'),
('ACCT334', 'Intermediate Financial Accounting'),
('ACCT335', 'Advanced Financial Accounting'),
('ACCT336', 'Valuation'),
('ACCT337', 'Statistical Programming'),
('ACCT401', 'Strategic Management Accounting'),
('ACCT403', 'Advanced Taxation'),
('ACCT407', 'Corporate Financial Management'),
('ACCT409', 'Auditing for the Public Sector'),
('ACCT410', 'Internal Audit(SMU-X)'),
('ACCT414', 'Accounting Analytics Capstone(SMU-X)'),
('ACCT416', 'Advanced Audit & Assurance'),
('ACCT417', 'Insolvency and Restructuring'),
('ACCT418', 'Data Modelling and Visualisation'),
('ACCT420', 'Forecasting and Forensic Analytics'),
('ACCT421', 'Analytics for Value Investing'),
('ACCT423', 'Audit Analytics(SMU-X)'),
('ACCT424', 'Auditing Information Systems(SMU-X)'),
('ACM003', 'Introduction to Arts and Cultural Management'),
('ACM004', 'Advanced Arts and Cultural Management(SMU-X)'),
('ACM101', 'Art & History I: From the Beginnings to the Revolutions'),
('ACM102', 'Art & History II: The Modern, Postmodern and the Contemporary'),
('ACM212', 'Arts and Cultural Marketing'),
('ACM213', 'Cultural Relations and Diplomacy in Asia'),
('ACM214', 'Arts, Culture Industries and Everyday Life(SMU-X)'),
('ACM301', 'Cultural Policy and Practice'),
('ANLY104', 'Analytics Foundation'),
('COMM102', 'Foundations in Strategic Communication'),
('COMM120', 'Intercultural Communication'),
('COMM121', 'Fundamentals of Media Engagement'),
('COMM225', 'Public Relations Writing'),
('COMM246', 'Crisis Management and Communication'),
('COMM253', 'Storytelling for Organisations and Brands(SMU-X)'),
('COMM254', 'Corporate Culture and Values(SMU-X: Philippines)'),
('COMM301', 'Data Analytics and Visualization for Communication Management'),
('COMM302', 'Designing Communication for Behavioural Change'),
('COMM334', 'Strategic Communication in Asia'),
('COMM346', 'Communication Strategies in the Digital Age'),
('COMM360', 'Investor Relations'),
('COMM361', 'The Business of the Creative Industries(SMU-X: New York)'),
('COR-COMM1304', 'Management Communication'),
('COR-IS1702', 'Computational Thinking'),
('COR-JPAN2401', 'Japanese'),
('COR-KREA2402', 'Korean'),
('COR-LAW2610', 'Constitutions, Cultures, and Context'),
('COR-LAW2612', 'Jurisprudence: Modern and Critical Theories of Law'),
('COR-MAND2404', 'Mandarin'),
('COR-MGMT1302', 'Business, Government and Society'),
('COR-MGMT2207', 'Innovations for Asia’s Smart Cities(SMU-X)'),
('COR-MLAY2405', 'Bahasa Melayu'),
('COR-POSC2604', 'Politics of South East Asia'),
('COR-PPPM2606', 'Sustainable Cities'),
('COR-SOCG2607', 'Contemporary South Asian Societies'),
('COR-SOCG2608', 'Understanding Chinas Economic Miracle: Social Origins and Social Impact'),
('COR-SOCG2609', 'Global and Transnational Sociology'),
('COR-STAT1202', 'Introductory Statistics'),
('COR-THAI2403', 'Thai'),
('COR1100', 'Writing and Reasoning'),
('COR1201', 'Calculus'),
('COR1301', 'Leadership and Team Building(SMU-X)'),
('COR1305', 'Spreadsheet Modeling and Analytics'),
('COR1306', 'Capital Markets in China'),
('COR1307', 'Accounting for Entrepreneurs(SMU-X)'),
('COR1701', 'Critical Thinking in the Real World'),
('COR1703', 'Managing in a Volatile, Uncertain, Complex and Ambiguous Context'),
('COR2100', 'Economics and Society'),
('COR2201', 'Technology and World Change'),
('COR2202', 'Science, Environment and Empire'),
('COR2203', 'Climate Change: Global and Local Solutions'),
('COR2204', 'Science and Technology Studies: Where Science meets Society'),
('COR2205', 'Climate, History and Society'),
('COR2208', 'Technological Solutions to Urban Challenges'),
('COR2209', 'Can Machines Think? AI in History, Philosophy, and Fiction'),
('COR2210', 'Technological Innovations Enhancing Urban Sustainability(SMU-X)'),
('COR2406', 'French'),
('COR2407', 'Italian'),
('COR2408', 'Spanish'),
('COR2601', 'Urban Cultures'),
('COR2603', 'Singapore: Imagining The Next Fifty Years'),
('COR2611', 'Cultural History of the Cold War in Asia'),
('COR2615', 'Finding Home in a Globalised World'),
('COR3001', 'Big Questions(Happiness and Suffering)'),
('COR3301', 'Ethics and Social Responsibility'),
('COR3302', 'Ethics and Social Responsibility for Accounting'),
('COR3303', 'Ethics and Social Responsibility for Law'),
('COR3304', 'Ethics and Corporate Responsibility'),
('CS101', 'Programming Fundamentals I'),
('CS102', 'Programming Fundamentals II'),
('CS103', 'Linear Algebra for Computing Applications'),
('CS104', 'Mathematical Foundations of Computing'),
('CS105', 'Statistical Thinking for Data Science'),
('CS106', 'Computer Hardware and Embedded Systems'),
('CS204', 'Interconnection of Cyber Physical Systems'),
('CS206', 'Software Product Management'),
('CS301', 'IT Solution Architecture'),
('CS420', 'Introduction to Artificial Intelligence'),
('CS421', 'Introduction to Machine Learning'),
('CS422', 'Reasoning, Planning and Learning under Uncertainty'),
('CS423', 'Heuristic Search and Optimisation'),
('CS424', 'Image Perception'),
('CS425', 'Natural Language Communication'),
('CS426', 'Agent-based Modeling and Simulation'),
('CS440', 'Foundations of Cybersecurity'),
('CS441', 'Network Security'),
('CS442', 'Data Security and Privacy'),
('CS443', 'Software and Systems Security'),
('CS444', 'Strategic Cybersecurity Management'),
('CS461', 'Mobile & Pervasive Computing and Applications'),
('CS462', 'Internet of Things: Technology and Applications(SMU-X)'),
('DSA201', 'Statistical Inference for Data Science'),
('DSA211', 'Statistical Learning with R'),
('DSA212', 'Data Science with R'),
('ECON101', 'Intermediate Microeconomics'),
('ECON102', 'Intermediate Macroeconomics'),
('ECON106Z', 'H3 Game Theory'),
('ECON107', 'Introduction to Econometrics'),
('ECON111', 'Microeconomics 1'),
('ECON113', 'Economics of Globalisation'),
('ECON118', 'Economic Development in Asia'),
('ECON145', 'Introductory Data Analytics in Healthcare'),
('ECON155', 'Healthcare Management'),
('ECON203', 'International Economics B'),
('ECON204', 'Development Economics'),
('ECON205', 'Intermediate Mathematics for Economics'),
('ECON206', 'Game Theory'),
('ECON207', 'Intermediate Econometrics'),
('ECON208', 'Industrial Organisation'),
('ECON209', 'Labour Economics'),
('ECON211', 'Public Sector Economics'),
('ECON212', 'Real Estate Economics'),
('ECON215', 'Health Economics(SMU-X)'),
('ECON216', 'Economics of Ageing'),
('ECON217', 'Macroeconomics of Income Distribution'),
('ECON218', 'Empirical Industrial Economics'),
('ECON220', 'Economic Growth'),
('ECON225', 'Health Systems and Policy'),
('ECON233', 'Economic Forecasting'),
('ECON234', 'International Trade'),
('ECON235', 'International Macroeconomics'),
('ECON236', 'Advanced Microeconomics'),
('ECON237', 'Advanced Macroeconomics'),
('ECON240', 'Family and the Society: Economic Theories and Practices(SMU-X)'),
('ECON241', 'Strategic Thinking'),
('ECON242', 'Political Economy Analysis of Institutions'),
('ECON315', 'Economic Dynamics'),
('ECON400', 'Senior Thesis'),
('FNAR001', 'Dance: East and West'),
('FNCE101', 'Finance'),
('FNCE102', 'Financial Markets and Investments'),
('FNCE103', 'Finance For Law'),
('FNCE201', 'Corporate Finance'),
('FNCE203', 'Analysis of Equity Securities'),
('FNCE204', 'Analysis of Fixed-Income Securities'),
('FNCE210', 'International Finance'),
('FNCE213', 'Entrepreneurial Finance'),
('FNCE217', 'Wealth Management and Advisory'),
('FNCE218', 'Wealth Management and the Law'),
('FNCE221', 'Investment Banking'),
('FNCE225', 'Consumer Banking'),
('FNCE229', 'Corporate Banking'),
('FNCE231', 'Real Estate Investments and Finance'),
('FNCE232', 'Project Financing'),
('FNCE234', 'Real Estate Valuation and Taxation'),
('FNCE235', 'Real Estate Development'),
('FNCE305', 'Analysis of Derivative Securities'),
('FNCE307', 'Advanced Portfolio Management'),
('FNCE310', 'Trade Finance'),
('FNCE313', 'Financial Innovation'),
('FNCE314', 'Sustainable Finance'),
('FNCE315', 'Analytics in Finance And Real Estate'),
('FTW100', 'Finishing Touch Workshops (Year One)'),
('FTW200', 'Finishing Touch Workshops (Year Two)'),
('GA001', 'Exploring Asian Identities'),
('GA002', 'Contemporary Asia: Power, Diversity & Change'),
('GA201', 'Popular Culture in Asia'),
('GA203', 'History of Southeast Asia'),
('GA205', 'Managing Diversity in Asia(SMU-X)'),
('GA305', 'Global Asia Study Mission'),
('HIST005', 'European Cultural History'),
('HUMN017', 'A Cultural Introduction to India: From Indus Valley to Infosys'),
('IDIS001', 'Analytical Skills'),
('IDIS100', 'Research Methods in Sociology and Political Science'),
('IDIS300', 'Scholars Study Mission(SMU-X: Germany)'),
('IDST302', 'Independent Study'),
('IS110', 'Information Systems and Innovation'),
('IS111', 'Introduction to Programming'),
('IS112', 'Data Management'),
('IS113', 'Web Application Development I'),
('IS210', 'Business Process Analysis Solutioning'),
('IS211', 'Interaction Design and Prototyping'),
('IS212', 'Software Project Management'),
('IS213', 'Enterprise Solution Development'),
('IS214', 'Enterprise Solution Management'),
('IS215', 'Digital Business - Technologies and Transformation'),
('IS216', 'Web Application Development II'),
('IS405', 'Technology Entrepreneurship Study Mission (Non-Asia)(SMU-X: USA)'),
('IS412', 'Enterprise Business Solutions(SMU-X)'),
('IS415', 'Geospatial Analytics and Applications'),
('IS419', 'Retail Banking and Mobile Technology'),
('IS423', 'Financial Markets Processes and Technology'),
('IS424', 'Data Mining and Business Analytics'),
('IS425', 'Managing Information Systems for Business Value(SMU-X)'),
('IS428', 'Visual Analytics for Business Intelligence(SMU-X)'),
('IS430', 'Digital Payments and Innovation'),
('IS434', 'Social Analytics and Applications(SMU-X)'),
('IS442', 'Object Oriented Programming'),
('IS444', 'Digital Banking Enterprise Architecture'),
('IS445', 'Corporate Banking Technology and Blockchain'),
('IS446', 'Managing Customer Relations with Analytics: Asian Insights'),
('IS447', 'Smart Healthcare in Asia(SMU-X)'),
('IS450', 'Text Mining and Language Processing'),
('IS451', 'Digital Analytics Technology'),
('IS470', 'Guided Research in Information Systems'),
('IS471', 'Guided Research in Computing 2'),
('IS480', 'IS Application Project(SMU-X)'),
('IS483', 'IS Project Experience (Applications)'),
('IS484', 'IS Project Experience [FinTech]'),
('IS490', 'Google Analytics Work-Study Elective'),
('LAW101', 'Contract Law 1'),
('LAW102', 'Contract Law 2'),
('LAW103', 'Criminal Law'),
('LAW105', 'Law of Torts'),
('LAW106', 'Legal Research and Writing I'),
('LAW107', 'Legal Research and Writing II'),
('LAW108', 'The Singapore Legal System'),
('LAW201', 'Law of Business Organisations'),
('LAW202', 'Law of Property'),
('LAW203', 'Comparative Legal Systems'),
('LAW204', 'Constitutional & Administrative Law'),
('LAW205', 'Corporate Law'),
('LAW301', 'Legal Theory & Philosophy'),
('LAW302', 'Commercial Conflict of Laws'),
('LAW303', 'Law of Equity & Trusts'),
('LAW307', 'Law of Evidence'),
('LAW400', 'Directed Research'),
('LAW4001', 'Shareholder Deals and Litigation'),
('LAW4002', 'Legal Analytics and Artificial Intelligence in Law(SMU-X)'),
('LAW4003', 'International and Comparative Secured Transactions Law'),
('LAW4004', 'Digital Intelligence for Lawyers'),
('LAW401', 'Intellectual Property Law'),
('LAW402', 'Chinese Contract Law'),
('LAW404', 'Public International Law'),
('LAW405', 'Information Technology and the Law'),
('LAW406', 'International Commercial Arbitration'),
('LAW410', 'World Trade Organization: Law and Policy'),
('LAW414', 'International Commercialisation of Intellectual Property Rights'),
('LAW416', 'International Moots 1(SMU-X)'),
('LAW417', 'Law of Mergers and Acquisitions'),
('LAW419', 'International and Comparative Criminal Justice'),
('LAW422', 'Trade and Investment Law'),
('LAW423', 'Maritime and Admiralty Law in International Commerce'),
('LAW425', 'Advocacy(SMU-X)'),
('LAW428', 'Family Law'),
('LAW429', 'Corporate Insolvency Law'),
('LAW430', 'International Moots 2(SMU-X: Philip C Jessup Moot)'),
('LAW433', 'Financial & Securities Regulation'),
('LAW438', 'Law Study Mission to Asia(SMU-X: Taiwan)'),
('LAW445', 'Principles of the Law of Restitution'),
('LAW447', 'International Construction Law'),
('LAW451', 'Pre-trial Practice in Civil Litigation'),
('LAW462', 'Introduction to Civil Procedure'),
('LAW466', 'Evidence, Litigation and the Criminal Process'),
('LAW469', 'Introduction to Chinese History, Culture, Economy, Politics and Law'),
('LAW476', 'Medical Law and Health Policy'),
('LAW477', 'Law and Psychology'),
('LAW478', 'Professional Mediation Skills'),
('LAW481', 'International Mediation Law and Practice(SMU-X)'),
('LAW482', 'Deal-making and Dispute Resolution: Negotiation in an Age of Disruption'),
('LAW483', 'Law & Regulation'),
('LAW486', 'Privacy and Data Protection Law'),
('LAW487', 'Topics in Financial Crime'),
('LAW489', 'Introduction to Law and Technology'),
('LAW490', 'International and Comparative Insolvency Law'),
('LAW491', 'Law and Digital Commerce(SMU-X)'),
('LAW493', 'Intellectual Property Law and Competition Law at Interplay'),
('LAW495', 'Compliance and Risk Management for Lawyers'),
('LAW497', 'Chinese Commercial Arbitration'),
('LAW498', 'State Courts Clerkship Programme'),
('LAW499', 'Legal Commentaries for Practice (Advanced Legal Writing)(SMU-X)'),
('LGST101', 'Business Law'),
('LGST201', 'Company Law'),
('LGST210', 'Law of Real Estate'),
('LGST223', 'Law of International Trade'),
('LGST233', 'Health Law and Medical Ethics'),
('MGMT004', 'Creative Thinking'),
('MGMT102', 'Strategy'),
('MGMT104', 'Corporate Entrepreneurship and Innovation'),
('MGMT106', 'Introduction to Organisations'),
('MGMT108', 'Introduction to Business Analytics'),
('MGMT205', 'International Business'),
('MGMT218', 'Entrepreneurship and Business Creation'),
('MGMT222', 'Family Business'),
('MGMT223', 'Social Entrepreneurship'),
('MGMT227', 'Managing Creativity in Organizations'),
('MGMT232', 'Business Consulting'),
('MGMT233', 'Leadership Seminar with CEOs'),
('MGMT235', 'Sustainability Management and Governance'),
('MGMT236', 'Managing Strategic Change'),
('MGMT237', 'Corporate Strategy'),
('MGMT239', 'Play in Invention and Culture'),
('MGMT240', 'Doing Business with Artificial Intelligence'),
('MGMT301', 'Business Study Mission (Asian Studies)(Malaysia)'),
('MGMT304', 'Entrepreneurial Leadership in Ethnic Chinese Business'),
('MGMT310', 'Leading New Ventures to Growth'),
('MGMT312', 'Asia Pacific Business'),
('MGMT317', 'Managing Process Improvement(SMU-X)'),
('MGMT318', 'Design Thinking and Innovation(SMU-X)'),
('MGMT319', 'Management of Technology and Innovation'),
('MGMT321', 'Business Study Mission (Globalisation)(Germany)'),
('MGMT322', 'International Corporate Governance and Strategy'),
('MGMT327', 'Entrepreneurship Practicum(SMU-X)'),
('MGMT330', 'The Design of Business(SMU-X)'),
('MGMT331', 'Management of Multinationals Across Asia(SMU-X)'),
('MGMT332', 'Approaching Business Knowledge through Classics'),
('MGMT337', 'Sustainability Study Mission (Asian Studies)(Malaysia)'),
('MGMT339', 'The Innovation and Entrepreneurship Ecosystem in China(SMU-X)'),
('MKTG101', 'Marketing'),
('MKTG102', 'Consumer Behaviour'),
('MKTG103', 'Marketing Research'),
('MKTG204', 'Services Marketing'),
('MKTG205', 'Advertising'),
('MKTG217', 'Strategic Brand Management'),
('MKTG219', 'Retail Management'),
('MKTG220', 'Digital Marketing(SMU-X)'),
('MKTG225', 'Customer Relationship Management'),
('MKTG227', 'Integrated Marketing Communications: A Brand Perspective'),
('MKTG228', 'Marketing Analytics'),
('MKTG234', 'Sustainable Marketing'),
('MKTG313', 'Pricing'),
('MKTG314', 'Retail Strategy'),
('OBHR101', 'Management of People at Work'),
('OBHR201', 'Human Capital Management'),
('OBHR202', 'Performance Management & Compensation'),
('OBHR203', 'Personnel Selection'),
('OBHR204', 'Training & Development'),
('OBHR212', 'Cross-Cultural Management & the Management of Diversity'),
('OBHR215', 'Organisational Change & Design'),
('OBHR222', 'Negotiation and Conflict Management'),
('OBHR224', 'Human Capital Strategy'),
('OBHR225', 'Technology Solutions for Human Resources'),
('OBHR228', 'The Psychology of Managerial Decision Making'),
('OBHR231', 'The Mosaic of Leadership'),
('OBHR232', 'Legal Environment and Employment Relations'),
('OBHR233', 'Millennial Talent Management Recruitment and Engagement(SMU-X: Indonesia)'),
('OBHR299', 'Special Topics in Organisational Behaviour'),
('OBHR300', 'Human Resources Analytics'),
('OPIM101', 'Decision Analysis'),
('OPIM201', 'Operations Management'),
('OPIM311', 'Service Processes'),
('OPIM313', 'Project Management'),
('OPIM314', 'Logistics and Transportation Management'),
('OPIM318', 'Sustainable Operations'),
('OPIM319', 'Operations Strategy: Principles and Practice'),
('OPIM321', 'Supply Chain Management'),
('OPIM322', 'High Performance Warehousing and Fulfillment'),
('OPIM324', 'Global Supply Chains'),
('OPIM325', 'Sales and Operations Planning'),
('OPIM326', 'Service and Operations Analytics'),
('OPIM341', 'Procurement and Strategic Sourcing'),
('OPIM343', 'Port-Focal Logistics and Maritime Operations'),
('OPIM344', 'Sustainable Shipping and Ports'),
('OPIM345', 'Decision Analysis 2 - Multi-criteria Decisions'),
('PHIL207', 'Introduction to Classical Chinese Philosophy'),
('PLE401', 'Senior Thesis in Politics, Law and Economics'),
('POSC003', 'Introduction to Political and Policy Studies'),
('POSC101', 'Introduction to Public Policy'),
('POSC103', 'World Politics'),
('POSC208', 'Security Studies'),
('POSC211', 'European Union Politics'),
('POSC215', 'Democracy'),
('POSC219', 'Political Theory'),
('POSC220', 'International Relations of East Asia'),
('POSC222', 'Chinese Foreign Policy'),
('POSC320', 'Elections and Media'),
('POSC322', 'Mass Media and Public Opinion Research'),
('POSC324', 'Media and International Relations'),
('POSC401', 'Senior Thesis in Political Issue'),
('PPPM101', 'Public Sector Management'),
('PPPM204', 'Political Participation and Policy'),
('PPPM205', 'Religion and Policy in Asia'),
('PPPM301', 'Public Policy Task Force(SMU-X: Anly Glob Palm Oil Ind)'),
('PSYC001', 'Introduction to Psychology'),
('PSYC104', 'Developmental Psychology'),
('PSYC105', 'Industrial and Organisational Psychology'),
('PSYC107', 'Psychology of Individual Differences'),
('PSYC108', 'Social Psychology'),
('PSYC110', 'Psychology Research Methods I'),
('PSYC112', 'Health Psychology'),
('PSYC202', 'Cultural Psychology'),
('PSYC204', 'Psychology of Reasoning & Thinking'),
('PSYC205', 'Evolutionary Psychology'),
('PSYC208', 'Psychology Research Methods II'),
('PSYC209', 'Psychology of Close Relationships'),
('PSYC307', 'Psychology Study Mission(SMU-X: Cul Impact on Creat Ind)'),
('PSYC401', 'Senior Thesis in Psychology'),
('QF101', 'Quantitative Finance'),
('QF102', 'Investment Statistics'),
('QF205', 'Computing Technology For Finance'),
('QF206', 'Quantitative Trading Strategies'),
('QF207', 'Structured Products Sales and Trading'),
('QF208', 'Linear Algebra and Numerical Methods'),
('QF305', 'Global Financial Risk Management'),
('QF307', 'Stochastic Finance'),
('SMT112', 'Sustainable Digital Cities'),
('SMT201', 'Geographic Information Systems for Urban Planning'),
('SMT202', 'Analytics Applications for Smart Living'),
('SMT203', 'Smart City Systems and Management'),
('SMT483', 'SMT Project Experience (Applications)(SMU-X)'),
('SOCG001', 'Understanding Societies'),
('SOCG110', 'Deconstructing Singapore Society'),
('SOCG201', 'Social Stratification and Inequality'),
('SOCG215', 'Introduction to Sociological Theory'),
('SOCG227', 'InterAsian Mobilities'),
('SOCG304', 'Social Networks'),
('SOCG307', 'Governance and Development in the Global South'),
('SPRT001', 'Principles of Coaching in Sports'),
('SSCS400', 'Capstone Seminar'),
('STAT151', 'Introduction to Statistical Theory'),
('STAT201', 'Probability Theory and Applications'),
('STAT203', 'Financial Mathematics'),
('STAT204', 'Survey Methods'),
('STAT310', 'Life Contingent Risks'),
('STAT311', 'Risk Theory and Loss Models'),
('STAT313', 'Quantitative Risk Analysis'),
('TRAD201', 'Shipping Business');

-- --------------------------------------------------------

--
-- Table structure for table `ModuleVerification`
--

DROP TABLE IF EXISTS `ModuleVerification`;
CREATE TABLE IF NOT EXISTS `ModuleVerification` (
  `email` varchar(255) NOT NULL,
  `module_code` varchar(255) NOT NULL,
  `module_grade` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `ModuleVerification`
--

INSERT INTO `ModuleVerification` (`email`, `module_code`, `module_grade`) VALUES
('b@gmail.com', 'IS111', 'A-'),
('b@gmail.com', 'IS210', 'A+'),
('p@gmail.com', 'IS111', 'A+'),
('p@gmail.com', 'IS210', 'A+');

-- --------------------------------------------------------

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
CREATE TABLE IF NOT EXISTS `User` (
  `email` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `password_salt` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `User`
--

INSERT INTO `User` (`email`, `name`, `password_salt`, `password_hash`) VALUES
('b@gmail.com', 'Brandon', '8a42bd59518f44e6ac9eecb37b2f4861', '03a952f730b0093c057a4e8a2b271f7d2f96463e317ad515719171804913f5840d8116b7f8175b85ec678de0ef53f2d8d065691ce0d0bd3cb0baafe5aafe42e0'),
('p@gmail.com', 'Phyo', 'af84c71a5f36434da76b398a9f297446', 'd63ebc52247b89d60600bcc36303738fd09e9ec6a6c2e1bbd64465d25059c475f32f1c5069e40e408b55a03c5188a58fcf4009b4928c445d32cdb711accb347e');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Bubble`
--
ALTER TABLE `Bubble`
  ADD PRIMARY KEY (`bubble_id`);

--
-- Indexes for table `BubbleComment`
--
ALTER TABLE `BubbleComment`
  ADD PRIMARY KEY (`bubble_id`,`email`,`timestamp`);

--
-- Indexes for table `BubbleFile`
--
ALTER TABLE `BubbleFile`
  ADD PRIMARY KEY (`bubble_id`,`timestamp`);

--
-- Indexes for table `BubbleRole`
--
ALTER TABLE `BubbleRole`
  ADD PRIMARY KEY (`bubble_id`,`email`);

--
-- Indexes for table `Log`
--
ALTER TABLE `Log`
  ADD PRIMARY KEY (`email`,`timestamp`);

--
-- Indexes for table `Module`
--
ALTER TABLE `Module`
  ADD PRIMARY KEY (`module_code`);

--
-- Indexes for table `ModuleVerification`
--
ALTER TABLE `ModuleVerification`
  ADD PRIMARY KEY (`email`,`module_code`);

--
-- Indexes for table `User`
--
ALTER TABLE `User`
  ADD PRIMARY KEY (`email`);
